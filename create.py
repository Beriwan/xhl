# coding=UTF-8

import os
import time
from datetime import datetime

from xhl.db import Mysql

class CreateTable(object):

    def set_table(self,tablename):
        anchor_table = '{tablename}_{date}'.format(tablename=tablename,date=datetime.now().strftime('%m%d'))
        sql5 = 'DROP TABLE IF EXISTS {table};'.format(table=anchor_table)
        sql = '''CREATE TABLE IF NOT EXISTS {table} LIKE {tablename};'''.format(table=anchor_table,tablename=tablename) #建新表
        sql1 = 'INSERT INTO {table} SELECT * FROM {tablename};'.format(table=anchor_table,tablename=tablename) #数据插入新表
        sql2 = 'DROP TABLE IF EXISTS {tablename};'.format(tablename=tablename) #删除旧表
        sql3 ='CREATE TABLE IF NOT EXISTS {tablename} LIKE {table};'.format(tablename=tablename,table=anchor_table) #
        mysql = Mysql()
        mysql.cursor.execute(sql5)
        mysql.create_table(sql)
        mysql.insert_one(sql1)
        mysql.cursor.execute(sql2)
        print('删除成功')
        mysql.create_table(sql3)
        mysql.close_db()


# DROP TABLE IF EXISTS anchor_test;
# CREATE TABLE IF NOT EXISTS anchor_test LIKE anchor_test_0627;

if __name__ == '__main__':
    run = CreateTable()
    run.set_table('user_detail')
    run.set_table('rank_history')
    run.set_table('anchor_test')
    run.set_table('anchor_detail')
    run.set_table('rich_id')
    print('successful')