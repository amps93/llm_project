import pymysql
import pandas as pd
from sqlalchemy import create_engine


class DataBase:
    def __init__(self, custom_info):
        self.host, self.port, self.id, self.pw, self.db = custom_info.values()

    def connect_db(self):
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.id,
                                    password=self.pw,
                                    database=self.db,
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor)

    def create(self, query):
        cur = self.conn.cursor()
        cur.execute(query)

    def select(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        res = cur.fetchall()

        result = pd.DataFrame(res)

        return result

    def insert(self, df, tb_name):
        engine = create_engine("mysql+pymysql://" + self.id + ":" + self.pw + "@" + self.host + ":" + str(
            self.port) + "/" + self.db + "?charset=utf8", encoding='utf-8')

        df.to_sql(name=tb_name, con=engine, if_exists='append', index=False)

    def truncate(self, tb_name):
        cur = self.conn.cursor()
        cur.execute('TRUNCATE TABLE ' + tb_name + ';')

    def drop(self, query):
        cur = self.conn.cursor()
        cur.execute(query)

    def close_connection(self):
        self.conn.close()
