import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


class NatePannLinkCrawler(object):
    def __init__(self, url):
        self.url = url
        self.date = (datetime.now() - timedelta(days=1)).strftime('%Y.%m.%d')
        self.before_date = (datetime.now() - timedelta(days=2)).strftime('%Y.%m.%d')
        self.day_before_date = (datetime.now() - timedelta(days=3)).strftime('%Y.%m.%d')
        self.session = requests.Session()

    def get_start_page(self):
        page = 1
        start_page = 0
        while True:
            webpage = self.session.get(self.url + "?page=" + str(page))
            soup = BeautifulSoup(webpage.content, "lxml")

            for j in soup.select('#searchDiv > div.posting_wrap > table > tbody > tr > td:nth-of-type(4)'):
                if j.text == self.date:
                    start_page = page
                elif j.text == self.before_date:
                    start_page = page

            if start_page > 0:
                break
            page += 1

            if page == 10:
                start_page = 1
                break

        return start_page

    def get_end_page(self, page):
        end_page = 0
        while True:
            webpage = self.session.get(self.url + "?page=" + str(page))
            soup = BeautifulSoup(webpage.content, "lxml")

            for j in soup.select('#searchDiv > div.posting_wrap > table > tbody > tr > td:nth-of-type(4)'):
                if j.text == self.before_date:
                    end_page = page
                elif j.text == self.day_before_date:
                    end_page = page

            if end_page == page:
                break

            page += 1

            if page == 30:
                end_page = 1
                break

        return end_page

    def crawling_nate_pann_link(self, page):
        webpage = self.session.get(self.url + "?page=" + str(page))
        soup = BeautifulSoup(webpage.content, "lxml")

        link_li = []
        date_li = []
        cate_li = []

        for subject in soup.select('.subject'):
            for a in subject.find_all('a'):
                if 'channel' not in a['href']:
                    link_li.append('https://pann.nate.com' + a['href'])

        for t in soup.select('#searchDiv > div.posting_wrap > table > tbody > tr > td:nth-of-type(4)'):
            date_li.append(t.text)
            cate_li.append(soup.select(
                '#container > div.content.sub > div.mainarea > div.post_pop > div.tit_category > h1 > span')[0].text)

        df = pd.DataFrame(zip(cate_li, link_li, date_li), columns=['category', 'link', 'pubDate'])

        return df

    def get_crawling_result(self, start_page, end_page):
        df_li = []
        for i in range(start_page, end_page + 1):
            df_li.append(self.crawling_nate_pann_link(i))
        df = pd.concat(df_li)
        df = df[df['pubDate'] == self.date].reset_index(drop=True)

        return df[['category', 'link', 'pubDate']]
