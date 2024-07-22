import pandas as pd
from nate_article_crawler import NateArticleCrawler
import os
import sys
from nate_pann_crawler import crawling_nate_pann
from starlette.config import Config

# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# print(parent_dir)
# print(sys.path)
# sys.path.append(parent_dir)

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from custom_def import save_file


def main(args):
    # env_config = Config(r'/home/ubuntu/recom/crawling/.env')
    env_config = Config(r'C:/Users/amps/python/llm_project/crawling/.env')
    save_path = env_config('nate_path')

    if args == 'nate_news':
        crawler = NateArticleCrawler()

        news_df = crawler.nate_news_crawler('NATE_NEWS')
        enter_df = crawler.nate_news_crawler('NATE_ENTERTAIN')
        sports_df = crawler.nate_news_crawler('NATE_SPORTS')

        nate_news_df = pd.concat([news_df, enter_df, sports_df], ignore_index=True)
        save_file(nate_news_df, save_path, 'nate_news.csv')

    elif args == 'nate_pann':
        nate_pann_df = crawling_nate_pann()
        save_file(nate_pann_df, save_path, 'nate_pann.csv')


if __name__ == '__main__':
    main(str(sys.argv[1]))

