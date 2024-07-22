import requests
from bs4 import BeautifulSoup
import time
import re
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


class NatePannContentsCrawler(object):
    def __init__(self):
        self.contents_dct = {
            'category': [],
            'link': [],
            'title': [],
            'description': [],
            'pub_date': []
        }
        self.session = requests.Session()

    @staticmethod
    def remove_html_tags(text):
        soup = BeautifulSoup(text, 'lxml')
        text = soup.get_text(separator=' ', strip=True)

        # 이모지 제거
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"
                                   u"\U0001F300-\U0001F5FF"
                                   u"\U0001F680-\U0001F6FF"
                                   u"\U0001F1E0-\U0001F1FF"
                                   "]+", flags=re.UNICODE)

        text = emoji_pattern.sub(r'', text)

        return re.sub(r'\s+', ' ', text)

    def crawling_nate_pann_contents(self, df_lst):
        for df in df_lst:
            for cate, link in zip(df['category'], df['link']):
                webpage = self.session.get(link)
                soup = BeautifulSoup(webpage.content, "lxml")
                try:
                    title = soup.select('#container > div.content.sub > div.viewarea > '
                                        'div.view-wrap > div.post-tit-info > h1')[0].text
                    self.contents_dct['title'].append(title)
                    self.contents_dct['category'].append(cate)
                    self.contents_dct['link'].append(link)
                    contents = soup.select('#contentArea')[0].text
                    contents = self.remove_html_tags(contents)
                    self.contents_dct['description'].append(contents)
                    self.contents_dct['pub_date'].append(soup.select('#container > div.content.sub > div.viewarea > '
                                                                     'div.view-wrap > div.post-tit-info > div.info > '
                                                                     'span.date')[0].text)
                except IndexError:
                    print(link)
                    continue

                time.sleep(0.5)
