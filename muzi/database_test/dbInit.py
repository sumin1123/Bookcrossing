# -*- coding: utf-8 -*-
import sqlite3

#SQLite数据库名
DB_SQLITE_NAME="bookcrossing.db"

def db_init():
    '''''
    Author: Justin
    Date: 2017-10-15
    Description: 创建数据库表
    '''

    # 连接数据库
    try:
        sqlite_conn = sqlite3.connect(DB_SQLITE_NAME)
    except sqlite3.Error as e:
        print("连接sqlite3数据库失败" + "\n" + e.args[0])
        # thxiami: 如果这里数据库连接失败，下面的代码就无法运行，所以这里直接返回，不执行下面的代码
        return
    # 获取游标
    sqlite_cursor = sqlite_conn.cursor()

    # 如果存在表先删除
    sql_users_del = "DROP TABLE IF EXISTS users;"
    sql_booklist_del = "DROP TABLE IF EXISTS book_list;"
    sql_bookdetails_del = "DROP TABLE IF EXISTS book_details;"
    try:
        sqlite_cursor.execute(sql_users_del)
        sqlite_cursor.execute(sql_booklist_del)
        sqlite_cursor.execute(sql_bookdetails_del)
    except sqlite3.Error as e:
        print("删除数据库表失败！" + "\n" + e.args[0])
    sqlite_conn.commit()

    # 创建表
    sql_users_add = '''CREATE TABLE users(
                    user_id INTEGER PRIMARY KEY autoincrement NOT NULL,
                    user_name text,
                    password text,
                    nickname text,
                    wechat_id text,
                    location text
                    );'''
    sql_booklist_add = '''CREATE TABLE book_list(
                    local_id INTEGER PRIMARY KEY autoincrement NOT NULL,
                    isbn int,
                    state int,
                    user_id int
                    );'''
    sql_bookdetails_add = '''CREATE TABLE book_details(
                    isbn INTEGER PRIMARY KEY NOT NULL,
                    douban_id int,
                    image text,
                    title text,
                    alt text,
                    author text,
                    publisher text,
                    tags text,
                    summary text,
                    global_id identity(1,1)
                    );'''

    try:
        sqlite_cursor.execute(sql_users_add)
        sqlite_cursor.execute(sql_booklist_add)
        sqlite_cursor.execute(sql_bookdetails_add)
    except sqlite3.Error as e:
        print("创建数据库表失败！" + "\n" + e.args[0])
        return
    sqlite_conn.commit()
    sqlite_conn.close()
    print('DB is initilized')


if __name__ == "__main__":
    db_init()
