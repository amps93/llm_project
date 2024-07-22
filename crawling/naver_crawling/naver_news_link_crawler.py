import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


class NaverLinkCrawler:
    def __init__(self, url):
        self.page = 0
        self.url = url
        self.date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        self.article_link_lst = []
        self.pcategory_lst = []
        self.category_lst = []
        self.session = requests.Session()
        self.headers = {'user-agent': "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) "
                                      "Chrome / 110.0.0.0Safari / 537.36"}

    def get_page_num(self):
        for i in range(1, 100, 10):
            url = self.url + 'date=' + str(self.date) + '&page=' + str(i)
            webpage = self.session.get(url, headers=self.headers)
            soup = BeautifulSoup(webpage.text, "lxml")

            current_page = soup.select('#main_content > div.paging')[0].find('strong').text
            if self.page == current_page:
                break
            self.page = current_page

    def get_article_link(self):
        for i in range(1, int(self.page) + 1):
            url = self.url + 'date=' + str(self.date) + '&page=' + str(i)
            html = self.session.get(url, headers=self.headers)
            soup = BeautifulSoup(html.text, "lxml")
            try:
                for i in range(1, 11):
                    self.article_link_lst.append(soup.select(
                        '#main_content > div.list_body.newsflash_body > ul.type06_headline > li:nth-of-type(' + str(
                            i) + ') > dl > dt > a')[0].attrs['href'])
                    self.article_link_lst.append(soup.select(
                        '#main_content > div.list_body.newsflash_body > ul.type06 > li:nth-of-type(' + str(
                            i) + ') > dl > dt > a')[0].attrs['href'])
                    self.pcategory_lst.append(soup.select('#snb > h2 > a')[0].text)
                    self.pcategory_lst.append(soup.select('#snb > h2 > a')[0].text)
                    self.category_lst.append(soup.select('#snb > ul')[0].find('li', {'class': 'on'}).text.split(' ')[0])
                    self.category_lst.append(soup.select('#snb > ul')[0].find('li', {'class': 'on'}).text.split(' ')[0])
            except:
                pass