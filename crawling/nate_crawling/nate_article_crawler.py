from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config as cfg


class NateArticleCrawler(object):
    def __init__(self):
        self.site_info = cfg.nate_crawler['nate_news_site_info']
        self.session = requests.Session()
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def nate_news_crawler(self, category_info):
        url = self.site_info[category_info]
        webpage = self.session.get(url)
        soup = BeautifulSoup(webpage.content, "html.parser")

        title_lst = []
        rank_lst = []

        titles_top5 = soup.select('.postRankSubjectList.f_clear h2.tit')
        ranks_top5 = soup.select('.postRankSubjectList.f_clear .mduSubjectList.f_clear dt em')
        for title, rank in zip(titles_top5, ranks_top5):
            title_lst.append(title.get_text(strip=True))
            rank_lst.append(rank.get_text(strip=True))

        titles_6_to_50 = soup.select('.postRankSubject h2')
        ranks_6_to_50 = soup.select('.postRankSubject dt em')
        for title, rank in zip(titles_6_to_50, ranks_6_to_50):
            title_lst.append(title.get_text(strip=True))
            rank_lst.append(rank.get_text(strip=True))

        df = pd.DataFrame({'type': category_info, 'rank': rank_lst, 'title': title_lst, 'regDate': self.current_time})

        return df
