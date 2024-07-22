import requests
from bs4 import BeautifulSoup
import time
import re
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


class NaverContentsCrawler:
    def __init__(self):
        self.title_lst = []
        self.description_lst = []
        self.pubdate_lst = []
        self.session = requests.Session()
        self.headers = {'user-agent': "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) "
                                      "Chrome / 110.0.0.0Safari / 537.36"}

    @staticmethod
    def remove_html_tags(text):
        cleantext = BeautifulSoup(text, "lxml").text  # html 태그 제거

        patterns = [
            r'\s+',
            r'\\n|\xa0',
            r'\[.*?기자\]',
            r'\s\(.*?기자\)',
            r'....기자',
            r'사진\s*=|\[사진\s*=',
            r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
            r'\(서울=.*?\)|\[서울=.*?\]',
            r'[\(\[][^\)\]]*연합뉴스[^\)\]]*[\)\]]',
            r'\[\[the300\]\]',
            r'연합뉴스|뉴스1',
            r'='
        ]

        # 이모지 제거
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"
                                   u"\U0001F300-\U0001F5FF"
                                   u"\U0001F680-\U0001F6FF"
                                   u"\U0001F1E0-\U0001F1FF"
                                   "]+", flags=re.UNICODE)

        cleantext = emoji_pattern.sub(r'', cleantext)

        for pattern in patterns:
            cleantext = re.sub(pattern, ' ', cleantext)

        return cleantext.strip()

    def crawling_naver_articles(self, df_lst):
        crawling_df_lst = []

        for df in df_lst:
            for link in df['link']:
                webpage = self.session.get(link, headers=self.headers)
                soup = BeautifulSoup(webpage.text, "lxml")

                # title
                try:
                    title = soup.find('h2', {'id': 'title_area'})
                    self.title_lst.append(title.text)
                except:
                    self.title_lst.append(None)

                # description
                try:
                    description = soup.find('div', {'id': 'dic_area'})
                    description = description.text
                    description = self.remove_html_tags(description)
                    self.description_lst.append(description)
                except:
                    self.description_lst.append(None)

                # pubdate
                try:
                    pubdate = soup.find('span', {'class': 'media_end_head_info_datestamp_time _ARTICLE_DATE_TIME'})
                    pubdate = pubdate['data-date-time']
                    self.pubdate_lst.append(pubdate)
                except:
                    self.pubdate_lst.append(None)

                time.sleep(1)

            df['title'] = self.title_lst
            df['description'] = self.description_lst
            df['pub_date'] = self.pubdate_lst

            crawling_df_lst.append(df)

            self.title_lst, self.description_lst, self.pubdate_lst = [], [], []

        return crawling_df_lst
