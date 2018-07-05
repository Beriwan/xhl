import time

import pymysql

MYSQL_HOST = '10.10.0.125'
#MYSQL_HOST = '192.168.0.175'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
#MYSQL_PASSWORD = 'root'
MYSQL_PASSWORD = '5560203@wstSpider!'
MYSQL_DB = 'xiaohulu'


class Mysql(object):

    def __init__(self,table_name='source_taobao_live_itemId'):
        self.connect()
        self.table_name = table_name

    def connect(self):
        try:
            self.db = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                      password=MYSQL_PASSWORD, db=MYSQL_DB, port=MYSQL_PORT, charset='utf8')
            self.cursor = self.db.cursor()
            self.cursor.execute('SET NAMES utf8mb4 ;')
            self.cursor.execute('SET CHARACTER SET utf8mb4 ;')
            self.cursor.execute('SET character_set_connection=utf8mb4 ;')
        except pymysql.Error as e:
            print('Error:%s' % e)

    def close_db(self):
        try:
            if self.db:
                self.db.close()
        except pymysql.Error as e:
            print('Error:%s' % e)

    def get_itemId(self):
        sql = 'select * from `{table_name}`'.format(table_name=self.table_name)
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        for item in data:
            yield item[0]
        # print(data)
        cursor.close()
        self.close_db()


    def get_two(self,sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        for item in data:
            yield item



    def get_shoplist(self,table = 'source_taobao_goods_detail'):
        sql = 'SELECT itemId FROM `{table}` GROUP BY shopId'.format(table=table)
        cursor = self.cursor
        cursor.execute(sql)
        data = cursor.fetchall()
        for item in data:
            yield item[0]
        # print(data)
        cursor.close()
        self.close_db()


    def insert_sql_many(self, sql, list):
        try:
            start = time.time()
            sql = sql
            self.cursor.executemany(sql, list)
            end1 = time.time()
            print(end1-start)
            self.db.commit()
            print("插入成功")
        except pymysql.Error as e:
            print(e)

    def insert_one(self, sql):
        # try:
        start = time.time()
        sql = sql
        self.cursor.execute(sql)
        end1 = time.time()
        # print(end1-start)
        self.db.commit()
        print("插入成功")
        # except pymysql.Error as e:
        #     print(e)


    def create_table(self, sql):
        try:
            self.cursor.execute(sql)
            print('创建成功')
        except Exception as e:
            print('error: %s' %e)



    def get_sql_sentence(self,tableName, item):
        COLstr = ''  # 列的字段
        for key in item.keys():
            COLstr = COLstr + '`{key}`'.format(key=key) + ','
        COLstr = COLstr[:-1]
        for _ in item:
            ROWstr = ''  # 行字段
            for key in item.keys():
                ROWstr = ROWstr + '\'{content}\''.format(content=item[key]) + ','
            ROWstr = ROWstr[:-1]
        COLstr = "({})".format(COLstr)
        ROWstr = "({})".format(ROWstr)
        return '{} {} VALUES {}'.format(tableName, COLstr, ROWstr)

if __name__ == '__main__':
    m = Mysql()
    m.get_two()