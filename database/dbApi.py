# coding:utf-8
import sqlite3
import json

"""
目前有6个函数
其功能，传入参数和返回值，返回值的格式都在 docstring 中写出
"""

# SQLite数据库名
DB_SQLITE_NAME="bookcrossing.db"

def insert_user_info(user_check_in):
    """
    功能：将用户注册的信息存入数据库（1）
    Args:
    user_check_in: 用户注册时的信息，数据类型dict。例如：{'user_name' : ['password', 'nickname', 'wechat', 'location']}
    """
    # 取出输入的字典参数值
    for k, v in user_check_in.items():
        userName = k
        userInfo = v

    user_name = userName
    password, nickname, wechat_id, location = userInfo[0], userInfo[1], userInfo[2], userInfo[3]

    # 连接数据库
    try:
        conn = sqlite3.connect(DB_SQLITE_NAME)
    except sqlite3.Error as e:
        print("连接sqlite3数据库失败" + "\n" + e.args[0])
        return

    # 获取游标
    sqlite_cursor = conn.cursor()

    # 添加一条记录
    sql_insert = "INSERT INTO users(user_name, password, nickname, wechat_id, location) \
                VALUES('%s', '%s', '%s', '%s', '%s')" % (user_name, password, nickname, wechat_id, location)
    try:
        sqlite_cursor.execute(sql_insert)
    except sqlite3.Error as e:
        print("添加用户数据失败！" + "\n" + e.args[0])
        return
    conn.commit()


def get_user_info(user_name=None):
    """
    功能：根据输入user_name得到对应的用户信息（2）
    Args:
    user_name: 用户名
    return:
    1. 如果用户已经注册，返回该用户对应的信息
    2. 如果用户没有注册，返回None
    """

    # 连接数据库
    try:
        conn = sqlite3.connect(DB_SQLITE_NAME)
    except sqlite3.Error as e:
        print("连接sqlite3数据库失败" + "\n" + e.args[0])
        return

    # 获取游标
    sqlite_cursor = conn.cursor()

    # 查询一条记录
    sql_select = "SELECT * FROM users WHERE user_name = user_name"
    try:
        sqlite_cursor.execute(sql_select)
        row = sqlite_cursor.fetchone()
    except sqlite3.Error as e:
        print("查询用户数据失败！" + "\n" + e.args[0])
        return

    # print("userInfo is: " + str(row[2]))
    return row


def get_user_books(user_id=None):
    """
    功能：根据 user_id 得到用户所有已发布的书的信息（3）
    Args:
        user_id(int): 用户id
    Return:
        # 1, 如果存在用户，不管是否发布过书，都按以下格式返回
        # 如果没发布过书， result 为 []
        {
            'state': 'success',
            'result': [{
                'local_id': 1,
                'isbn': 9999,
                'state': 'xx',
                'image': 'https://xx.xx.com/xxx.jpg',
                'title': 'xx',
                },{
                'local_id': 2,
                'isbn': 6666,
                'state': 'xx',
                'image': 'https://xx.xx.com/xxx.jpg',
                'title': 'xx',
                },
            ]
        }
        # 2, 如果不存在用户，返回以下格式
        {
            'state': 'failure',
            'result': 'User not found.'
        }



    result = []

    conn = sqlite3.connect('bookcrossing.db')
    c = conn.cursor()
    c.execute("SELECT local_id, isbn, state, user_id FROM book_list WHERE user_id=?", (user_id))
    #c.execute("SELECT user_id, user_name, password, nickname, wechat_id, location FROM users WHERE user_id=?", (user_id))
    rows = c.fetchall()

    if rows:
        for row in rows:
            result.append(row)
    else:
        result = 'User not found.'

    return result
    """

    pass



def get_books_detail(local_id=None):
    """
    功能：根据 local_id 得到数据库内相关书的详细信息（4）
    Args:
        local_id(int): 书籍 local_id
    Return:
        # 1, 如果数据库有对应的书，返回
        {
            'state': 'success',
            'result': {
                'user_info': {
                    'user_id': 123,
                    'nickname': 'xx',
                    'location': 'xx',
                    'wechat': 'xx',
                },
                'book_info': {
                    # 以下为 local_shelf 表中数据
                    'local_id': 1,
                    'isbn': 1234,
                    'state': 'xx',
                    # 以下为 global_shelf 表中数据
                    'image': 'https://xx.xx.com/xxx.jpg',
                    'title': 'xx',
                    'author': 'xx',
                    'publisher': 'xx',
                    'alt': 'https://book.douban.com/xx/',
                    'summary': 'xx'
                }
            }
        }
        # 2, 如果数据库没有对应的书, 返回
        {
            'state': 'failure',
            'result': 'Book not found.'
        }
    """

    pass


def get_books_list(isbn=None, title=None):
    """
    功能：用户输入 isbn 或者 title 检索数据库内是否有相关书籍
    根据 isbn 或者 title 检索，每次检索的条件只有一个，其中
        isbn 全部匹配
        title 模糊查找，部分匹配即可。如果实现困难则改为全部匹配（5）
    Args:
        isbn(int): 书籍 isbn 号
        title(str): 书名
    Return:
        # 1, 如果数据库有相关的书
        {
            'state': 'success',
            'result': [{
                # 第 1 本匹配的书籍
                # 以下为 local_shelf 表中数据
                'local_id': 1,
                'isbn': 1234,
                'state': 'xx',
                # 以下为 global_shelf 表中数据
                'image': 'https://xx.xx.com/xxx.jpg',
                'title': 'xx'
                },
                # 第 2 本匹配的书籍，相同的格式
                {...},
            ]
        }
        # 2, 如果数据库没有对应的书, 返回
        {
            'state': 'failure',
            'result': 'Book not found.'
        }
    """

    pass


def insert_book(users_id=None, local_id=None):
    """
    功能：用户发布共享书（6）
    Args:
        users_id(int): 发起书籍共享请求的用户的id， User 表的主键
    Return:
        # 1, 存在该书籍，书籍发布人是删除者，成功删除书籍
        {
            'state': 'success',
            'result': 'Book deleted successfully.'
        }
        # 2, 存在该书籍，但是书籍发布人不是删除者，不删除
        {
            'state': 'denied',
            'result': 'Book deleted failed. It belongs to others.'
        }
        # 3, 不存在该书籍
        {
            'state': 'notfound',
            'result': 'Book not found.'
        }
    """

    pass


def delete_book(users_id=None, local_id=None):
    """
    功能：用户删除已发布的书（7）
    Args:
        users_id(int): 发起删除请求的用户的 id， User 表的主键
        local_id(int): 书籍识别号， Local_shelf 表的主键
    Return:
        # 1, 存在该书籍，书籍发布人是删除者，成功删除书籍
        {
            'state': 'success',
            'result': 'Book deleted successfully.'
        }
        # 2, 存在该书籍，但是书籍发布人不是删除者，不删除
        {
            'state': 'denied',
            'result': 'Book deleted failed. It belongs to others.'
        }
        # 3, 不存在该书籍
        {
            'state': 'notfound',
            'result': 'Book not found.'
        }
    """

    pass


if __name__ == "__main__":
    # 测试函数 1
    test_user1 = {'张旭' : ['123456', 'Justin', 'good123', '北京']}
    insert_user_info(test_user1)

    # 测试函数 2
    userInfo = get_user_info('张旭')
    print("The user ID is: " + str(userInfo[0]))
