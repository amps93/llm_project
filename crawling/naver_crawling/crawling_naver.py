import requests.exceptions

from naver_news_link_crawler import NaverLinkCrawler
from naver_news_contents_crawler import NaverContentsCrawler
import pandas as pd
import os
import sys
from datetime import datetime, timedelta
import time

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config as cfg


def make_link_df(link_dct):
    df_lst = []
    for category in link_dct:
        for cate in link_dct[category]:
            crawler = NaverLinkCrawler(link_dct[category][cate])
            crawler.get_page_num()
            crawler.get_article_link()
            df_lst.append(pd.DataFrame(zip(crawler.pcategory_lst, crawler.category_lst, crawler.article_link_lst),
                                       columns=['p_category', 'category', 'link']))

    return df_lst


def fit_data_for_sql(df, link_col, date_col):
    date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    df = df.dropna()
    df = df.drop_duplicates(subset=[link_col])
    df = df[df[date_col] > date].sort_values(by=['p_category', 'category', 'pub_date']).reset_index(drop=True)

    return df


def main():
    max_retries = 5
    retry_delay_seconds = 60
    crawling_df_lst = []
    crawler = NaverContentsCrawler()

    for i in range(max_retries):
        try:
            article_link_df_lst = make_link_df(cfg.naver_crawler['naver_cate_link_dct'])
            crawling_df_lst = crawler.crawling_naver_articles(article_link_df_lst)
            break
        except(requests.exceptions.RequestException, OSError) as e:
            print(f'Error: {e}. Retrying in {retry_delay_seconds} seconds...')
            time.sleep(retry_delay_seconds)

    crawling_df = pd.concat(crawling_df_lst, ignore_index=True)
    crawling_df = crawling_df[['pub_date', 'p_category', 'category', 'link', 'title', 'description']]

    crawling_df = fit_data_for_sql(crawling_df, 'link', 'pub_date')

    dir_path = cfg.save_path['server']['naver']

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        crawling_df.to_csv(dir_path + 'naver_news.csv', index=False, encoding='utf8')
    else:
        crawling_df.to_csv(dir_path + 'naver_news.csv', index=False, encoding='utf8')
