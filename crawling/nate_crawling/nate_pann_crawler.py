from nate_pann_link_crawler import NatePannLinkCrawler
from nate_pann_contents_crawler import NatePannContentsCrawler
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config as cfg


def slice_description(df, n):
    for index, row in df.iterrows():
        if not isinstance(row['description'], float) and len(row['description']) > n:
            df.at[index, 'description'] = row['description'][:n]

    return df


def crawling_nate_pann():
    df_link_lst = []

    for key in cfg.nate_crawler['nate_pann_site_info']:
        link_crawler = NatePannLinkCrawler(cfg.nate_crawler['nate_pann_site_info'][key])
        s_page = link_crawler.get_start_page()
        e_page = link_crawler.get_end_page(s_page)
        df = link_crawler.get_crawling_result(s_page, e_page)
        df_link_lst.append(df)

    contents_crawler = NatePannContentsCrawler()
    contents_crawler.crawling_nate_pann_contents(df_link_lst)

    contetns_dct = contents_crawler.contents_dct

    df = pd.DataFrame(contetns_dct).drop_duplicates(subset=['link']).sort_values(by=['category', 'pub_date'])\
        .reset_index(drop=True)
    df = df[['pub_date', 'category', 'link', 'title', 'description']]
    df = slice_description(df, 3000)

    return df
