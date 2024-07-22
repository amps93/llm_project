import pandas as pd
from my_db import DataBase
import sys
from starlette.config import Config

import config as cfg


def insert_data_to_db(server, df, table):
    db = DataBase(server)
    db.connect_db()

    db.insert(df, table)
    db.close_connection()


def setting():
    env_config = Config(r'/home/ubuntu/recom/crawling/.env')
    nate_save_path = env_config('nate_path')
    naver_save_path = env_config('naver_path')
    daum_save_path = env_config('daum_path')
    server_setting = env_config('server')
    db_setting = env_config('db_server')

    return nate_save_path, naver_save_path, daum_save_path, server_setting, db_setting


def main(args):
    nate_save_path, naver_save_path, daum_save_path, server_setting, db_setting = setting()
    # 로그 디비 insert > naver, nate_pann
    # 웹 운영 insert > nate_news, daum_news
    if args == 'daum_nate_news':
        db_info = cfg.db_config['web_real']
        nate_news_df = pd.read_csv(nate_save_path + 'nate_news.csv')
        daum_news_df = pd.read_csv(daum_save_path + 'daum_news.csv')

        insert_data_to_db(db_info, nate_news_df, 'tbDaumNewsTitle')
        insert_data_to_db(db_info, daum_news_df, 'tbDaumNewsTitle')

    elif args == 'naver_nate_pann':
        db_info = cfg.db_config[db_setting]  # log_recom
        # naver_df = pd.read_csv(naver_save_path + 'naver_news.csv')
        nate_pann_df = pd.read_csv(nate_save_path + 'nate_pann.csv')

        # insert_data_to_db(db_info, naver_df, 'naver_news')
        insert_data_to_db(db_info, nate_pann_df, 'nate_news')


if __name__ == '__main__':
    main(str(sys.argv[1]))

