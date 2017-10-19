# coding:utf-8
import sqlite3
import json

"""
目前有8个函数
其功能，传入参数和返回值，返回值的格式都在 docstring 中写出
"""

# SQLite数据库名
DB_SQLITE_NAME="bookcrossing.db"

def insert_user_info(user_check_in):
    """
    功能：将用户注册的信息存入数据库（1）
    Args:
    user_check_in: 用户注册时的信息，数据类型dict。例如：{'user_name' : ['password', 'nickname', 'wechat', 'location']}
    Return:
        # 1, 发布成功则返回1
        # 2, 发布失败则返回0
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
        return 0

    # 获取游标
    sqlite_cursor = conn.cursor()

    # 添加一条记录
    sql_insert = "INSERT INTO users(user_name, password, nickname, wechat_id, location) \
                VALUES('%s', '%s', '%s', '%s', '%s')" % (user_name, password, nickname, wechat_id, location)
    try:
        sqlite_cursor.execute(sql_insert)
    except sqlite3.Error as e:
        print("添加用户数据失败！" + "\n" + e.args[0])
        return 0

    conn.commit()
    return 1


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
    sql_select = "SELECT * FROM users WHERE user_name = ?"
    try:
        sqlite_cursor.execute(sql_select, (user_name,))
        row = sqlite_cursor.fetchone()
    except sqlite3.Error as e:
        print("查询用户数据失败！" + "\n" + e.args[0])
        return 0

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
        # 3, 如果查询失败，返回0
    """

    result = []

    # 连接数据库
    try:
        conn = sqlite3.connect(DB_SQLITE_NAME)
    except sqlite3.Error as e:
        print("连接sqlite3数据库失败" + "\n" + e.args[0])
        return

    # 获取游标
    sqlite_cursor = conn.cursor()

    # 查询一条记录
    sql_select = "SELECT local_id, isbn, state, user_id FROM book_list WHERE user_id = user_id"
    try:
        sqlite_cursor.execute(sql_select)
        rows = sqlite_cursor.fetchall()
        if rows:
            for row in rows:
                result.append(row)
            resultReturn = {'state': 'success', 'result': result}
        else:
            #result = 'User not found.'
            resultReturn = {'state': 'failure', 'result': 'User not found.'}
    except sqlite3.Error as e:
        print("查询用户数据失败！" + "\n" + e.args[0])
        return 0

    return resultReturn


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


def insert_book(isbn, state=1, user_id=None):
    """
    功能：用户发布共享书（6）
    Args:
        users_id(int): 发起书籍共享请求的用户的id， User 表的主键
    Return:
        # 1, 发布成功则返回1
        # 2, 发布失败则返回0
    """
    # 连接数据库
    try:
        conn = sqlite3.connect(DB_SQLITE_NAME)
    except sqlite3.Error as e:
        print("连接sqlite3数据库失败" + "\n" + e.args[0])
        return

    # 获取游标
    sqlite_cursor = conn.cursor()

    # 添加一条记录
    sql_insert = "INSERT INTO book_list(isbn, state, user_id) \
                VALUES('%s', '%s', '%s')" % (isbn, state, user_id)
    try:
        sqlite_cursor.execute(sql_insert)
    except sqlite3.Error as e:
        print("添加用户书籍失败！" + "\n" + e.args[0])
        return 0

    conn.commit()
    return 1


def delete_book(users_id=None, local_id=None):
    """
    功能：用户删除已发布的书（7）
    Args:
        users_id(int): 发起删除请求的用户的 id， users 表的主键
        local_id(int): 书籍识别号， book_list 表的主键
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


def insert_book_details(bookInfo):
    """
    功能：插入书籍详情，来自豆瓣（8）
    Args:
        bookInfo: 列表类型，里面包含[isbn, douban_id, image, title, alt, author, publisher, tags, summary, global_id]
    Return:
        # 1, 插入成功则返回1
        # 2, 插入失败则返回0
    """
    # 连接数据库
    try:
        conn = sqlite3.connect(DB_SQLITE_NAME)
    except sqlite3.Error as e:
        print("连接sqlite3数据库失败" + "\n" + e.args[0])
        return

    # 获取游标
    sqlite_cursor = conn.cursor()

    # 添加一条记录
    sql_insert = "INSERT INTO book_details(isbn, douban_id, image, title, alt, author, publisher, tags, summary, global_id) \
                VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                % (bookInfo[0], bookInfo[1], bookInfo[2], bookInfo[3], bookInfo[4], bookInfo[5], bookInfo[6], bookInfo[7], bookInfo[8], bookInfo[9])
    try:
        sqlite_cursor.execute(sql_insert)
    except sqlite3.Error as e:
        print("添加书籍详情失败！" + "\n" + e.args[0])
        return 0

    conn.commit()
    return 1


def test_insert_user_info():
    # 测试函数 1
    test_user1 = {'张旭' : ['123456', 'Justin', 'good123', '北京']}
    test_user2 = {'xiami' : ['123456', 'xiami', 'good123', '北京']}
    test_user3 = {'test' : ['123456', 'test', 'good123', '北京']}

    for i in [test_user1, test_user2, test_user3]:


        if insert_user_info(i):
            print("insert_user_info function(1) passed")
        else:
            print("insert_user_info function(1) failed")


def test_get_user_info(user_name):
    # 测试函数 2
    userInfo = get_user_info(user_name)
    print('userInfo:', userInfo)
    if userInfo:
        print("get_user_info function(2) passed")
    else:
        print("get_user_info function(2) failed or user not registered")


if __name__ == "__main__":
    test_insert_user_info()

    test_get_user_info('xiami')

    """
    # 以下测试函数都可以类似上面写入为一个单独的函数进行测试
    # 这样便于单独测试某个函数，不需要测试时在这里注释掉即可
    # 测试时候可以配合使用 assert ，同时输出测试失败的原因和测试数据
    
    # 测试函数 6
    userInfo = get_user_info('张旭')
    if insert_book("1234567891234", "1", userInfo[0]) and insert_book("9999999999999", "1", userInfo[0]):
        print("insert_book function(6) passed")
    else:
        print("insert_book function(6) failed")

    # 测试函数 8
    book1 = [1234567891234, 22, 'http://g.com', 'My god', 'story to say', 'Tom', '', '', '', '']
    if insert_book_details(book1):
        print("insert_book_details function(8) passed")
    else:
        print("insert_book_details function(8) failed")
<<<<<<< HEAD

    # 测试函数3
    userBooks = get_user_books(userInfo[0])
    print("User books are: ", userBooks)
=======
    """
>>>>>>> e0d28d167fecf7a4a6e86147431b4305f4943038
