# coding:utf-8
'''
todo:
数据库 init 时的列名和类型以 config 形式存储下来，
insert_book_details 对传入的参数 book_details_dict 根据 key 取值时， key 就直接取 config 就可以
    然后 插入数据库时，SQL语句中的表名可以用格式化字符串取自  config
'''

'''
目前database/ 下的 api 函数有几个问题：
1， 每次调用函数都要重新连接一次数据库，这样影响性能，建议函数的传入参数第一个设置为 connection，传入数据库连接。
2，sql 语句内需要传参数时， 建议不适用 python 的字符串格式化来完成，可能会存在 sql 注入问题
    建议使用 sqlite3 模块提供的方法完成：

def selet(connection, user_email)
    sql_select = """
        SELECT
            *
        FROM
            user
        WHERE
            name=?
    """
    cursor = connection.cursor()
    row = cursor.execute(sql_insert, (user_email, )).fetchone() # 这里的 (username, ) 是一个 tuple

3，sqlite3 默认返回数据格式是不带有其列名的，返回的是一个 tuple，比如 搜索用户信息时， 游标返回的result是：
userInfo: (2, 'xiami', '123456', 'xiami', 'good123', '北京')

可以通过以下函数来修改返回结果的格式，源于官方推荐的方法

def dict_factory(cursor, row):
    """改变使用游标查询返回结果的类型为 dict，储存值类型为 {列名:值}"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect(path):
    """连接数据库，当不存在时创建并连接"""
    conn = sqlite3.connect(path)
    # 改变查询返回的数据为 dict 格式
    conn.row_factory = dict_factory
    return conn

4，建议可以试试使用 SQLAlchemy 来完成数据库方面的初始化，增删改查。
   这样不需要关心数据库的 sql语句的拼接，初学阶段可以避免一些错误，还有一个很大的优点：后期切换 MySQL 或其他关系型数据库时改动较小
'''
import os
import sqlite3

from models import (
    User,
    BookDetails,
    BookList,
)
from bookshelf import db

db_path = '/Users/xiami/PycharmProjects/Bookcrossing/database/test.sqlite'
DB_SQLITE_NAME = db_path


def dict_factory(cursor, row):
    """改变使用游标查询返回结果的类型为 dict，储存值类型为 {列名:值}"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect(path):
    """连接数据库，当不存在时创建并连接"""
    conn = sqlite3.connect(path)
    # 改变查询返回的数据为 dict 格式
    conn.row_factory = dict_factory
    return conn

'''
def get_user_books(user_id=None):
    """
    根据 users_id 得到用户所有已发布的书的信息

    Args:
        user_id(int): 用户id

    Return:
        # 1, 如果存在用户，而且发布过书，按以下格式返回
        {
            'status_code': '200',
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
        # 如果存在用户，但是没发布过书
        {
            'status_code': 'B01',
            'msg': 'The user hasn't released book. '
        }
        # 2, 如果不存在用户，返回以下格式
        {
            'status_code': 'U01',
            'msg': 'User not found.'
        }
    """
    if user_id == 1 or user_id ==2:
        # 如果存在该用户, 且发布过书
        result = {
            'status_code': '200',
            'result': [{
                'local_id': 1,
                'isbn': 9999,
                'state': 'xx',
                'image': 'https://img1.doubanio.com/mpic/s29543659.jpg',
                'title': 'xx',
                },{
                'local_id': 2,
                'isbn': 6666,
                'state': 'xx',
                'image': 'https://img3.doubanio.com/mpic/s29536350.jpg',
                'title': '书名',
                },
            ]
        }

    elif user_id == 3:
        # 如果存在用户，但是没发布过书
        result = {
            'status_code': 'B01',
            'msg': "The user hasn't released book.",
        }
    else:
        # 如果不存在该用户
        result = {
            'status_code': 'U01',
            'msg': 'User not found.',
        }
    return result
'''

def get_user_books(user_id=None):
    """
    功能：根据 user_id 得到用户所有已发布的书的信息（3）
    Args:
        user_id(int): 用户id
    Return:
        # 1, 如果存在用户，不管是否发布过书，都按以下格式返回
        # 如果没发布过书， result 为 []
        {
            'status': 'success',
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
            'status': 'failure',
            'result': 'User not found.'
        }
        # 3, 如果查询失败，返回0
    """

    conn = connect(db_path)
    result = []


    # 获取游标
    sqlite_cursor = conn.cursor()

    # 查询一条记录
    sql_select = '''
      SELECT
        book_list.isbn AS isbn, local_id, state, image, title
      FROM 
        book_list
      INNER JOIN 
        book_details 
      ON 
        book_list.user_id = ? AND book_list.isbn = book_details.isbn
    '''
    try:
        sqlite_cursor.execute(sql_select, (user_id,))
        rows = sqlite_cursor.fetchall()
        if rows:
            for row in rows:
                result.append(row)
            resultReturn = {'status': 'success', 'result': result}
        else:
            #result = 'User not found.'
            resultReturn = {'status': 'failure', 'result': 'User not found.'}
    except sqlite3.Error as e:
        print("查询用户数据失败！" + "\n" + e.args[0])
        return 0

    return resultReturn


def get_book_details(local_id=None):
    """
    根据 local_id 得到数据库内相关书的详细信息

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
    local_book = BookList.query.filter_by(local_id=local_id).first()

    if not local_book:
        # 没有这本书
        search_result = {
            'status': 'failure',
            'result': 'Book not found.'
        }
    else:
        # 有这本书
        book_owner = User.query.filter_by(id=local_book.user_id).first()
        global_book = BookDetails.query.filter_by(isbn=local_book.isbn).first()
        print('debug** get_book_details globalbook:', global_book)
        search_result= {
            'status': 'success',
            'result': {
                'user_info': {
                    'user_id': local_book.user_id,
                    'nickname': book_owner.nickname,
                    'location': book_owner.location,
                    'wechat': book_owner.wechat,
                },
                'book_info': {
                    # 以下为 local_shelf 表中数据
                    'local_id': local_id,
                    'isbn': local_book.isbn,
                    'state': local_book.state,
                    # 以下为 global_shelf 表中数据
                    'image': global_book.image,
                    'title': global_book.title,
                    'author': global_book.author,
                    'publisher': global_book.publisher,
                    'alt': global_book.alt,
                    'summary': global_book.summary
                }
            }
        }
    return search_result


def get_books_list(isbn=None, title=None):
    """
    用户输入 isbn 或者 title 检索数据库内是否有用户发布过相关书籍
    根据 isbn 或者 title 检索，每次检索的条件只有一个，其中
        isbn 全部匹配
        title 模糊查找，部分匹配即可。如果实现困难则改为全部匹配

    Args:
        isbn(int): 书籍 isbn 号
        title(str): 书名

    Return:
        # 1, 如果用户发布过相关的书
        {
            'status': 'success',
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

        # 2, 如果用户没有发布过对应的书, 返回
        {
            'status': 'failure',
            'result': 'Book not found.'
        }
    """
    if isbn is not None:
        # 根据 isbn 去两个表中拿到对应的书的信息
        book_list_instances = BookList.query.filter_by(isbn=isbn).all()  # [instance1, instance2, ...]
        book_details_instance = BookDetails.query.filter_by(isbn=isbn).first()  # instance

        # print('debug** get_books_list book_details_instance:{} '.format(book_details_instance))
        if len(book_list_instances) > 0 and book_details_instance is not None:
            # 两个表中都有数据
            book_list = []
            for b in book_list_instances:
                book_list.append(dict(
                    local_id=b.local_id,
                    state=b.state,
                    image=book_details_instance.image,
                    title=book_details_instance.title,
                    )
                )

            return dict(status='success', result=book_list)

    if title is not None:
        # 根据 title 去 book_details 表中找是否有这本书
        # 模糊搜索所以可能会在 book_details 表中搜索到多本书
        book_details_instances = BookDetails.query.filter(BookDetails.title.contains(title)).all()  # [instance1, instance2, ...]
        print("debug** get_books_list book_details 中搜索到的实例有:", book_details_instances)

        if len(book_details_instances) > 0:
            # 说明搜索到了书
            book_list = []
            for ins in book_details_instances:
                # 根据在 book_details 被搜索到的每一本书，去 book_list 表中找用户发布的书的信息，组成最终的 list
                temp_book_list = get_book_list_by_details_instance(book_details_instance=ins)
                book_list.extend(temp_book_list)

            if len(book_list) > 0:
                # 说明有用户发布过书
                return dict(status='success', result=book_list)

    # 没有找到书
    return dict(status='failure', result='Book not found')


def get_book_list_by_details_instance(book_details_instance=None):
    """
    根据 BookDetails 实例找到与之对应的 BookList 中的书的信息，组装为list返回
    :param book_details_instance: BookDetails 实例（Flask-SQLAlchemy 创建的class BookDetails）
    :return:
            1, 如果 BookList 中有对应的书，可能是多本相同的书，返回 元素为 dict 的 list
            [
            {
              "local_id": 1,
              "state": 1,
              "image": "https://img1.doubanio.com/mpic/s29539567.jpg",
              "title": "xx"
            },
            {
              "local_id": 2,
              "state": 1,
              "image": "https://img1.doubanio.com/mpic/s29539567.jpg",
              "title": "xx"
            },
            {
              "local_id": 3,
              "state": 1,
              "image": "https://img1.doubanio.com/mpic/s29539567.jpg",
              "title": "xx"
            }
           ]
          2, 如果 BookList 中没有对应的书，返回 []
    """
    isbn = book_details_instance.isbn
    book_list_instances = BookList.query.filter_by(isbn=isbn).all()  # [instance1, instance2, ...]

    # 用来存放书籍信息的 list
    book_list = []
    if len(book_list_instances) > 0:
        # 有用户发布过这本书
        for b in book_list_instances:
            book_list.append(dict(
                local_id=b.local_id,
                state=b.state,
                image=book_details_instance.image,
                title=book_details_instance.title,
                )
            )

    return book_list


def delete_book(local_id=None):
    """
    功能：用户删除已发布的书（7）
    Args:
        local_id(int): 书籍识别号， book_list 表的主键

    Return:
        # 1, 存在该书籍, 成功删除书籍
        {
            'status': 'success',
            'result': 'Book deleted successfully.'
        }
        # 2, 不存在该书籍
        {
            'status': 'failure',
            'result': 'Book not found.'
        }
        # 3, 其他异常情况，服务端需要记录错误日志
        {
            'status': 'failure',
            'result': 'unknown error'
        }
    """
    book = BookList.query.filter_by(local_id=local_id).first()

    if not book:
        # 如果没有查找到对应但是书籍
        result = {
            'status': 'failure',
            'result': 'Book not found.'
        }

    else:
        try:
            db.session.delete(book)
            db.session.commit()
            result = {
                'status': 'success',
                'result': 'Book deleted successfully.'
            }
        except Exception as e:
            # 服务器需要记录这个错误日志
            # app.logger.error(e)
            result = {
                'status': 'failure',
                'result': 'unknown error'
            }
    return result


def insert_book_list(isbn=None, state=1, user_id=None):
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
        return 0

    # 获取游标
    sqlite_cursor = conn.cursor()

    # 添加一条记录
    sql_insert = "INSERT INTO book_list(isbn, state, user_id) \
                VALUES(?,?,?)"

    try:
        sqlite_cursor.execute(sql_insert, (isbn, state, user_id))
        conn.commit()

    except sqlite3.Error as e:
        print("添加用户书籍失败！" + "\n" + e.args[0])
        return 0


    return 1


def insert_book_details(book_details_dict):
    """
    功能：插入书籍详情，来自豆瓣（8）
    Args:
        book_details_dict: 字典类型，里面 keys 包含[isbn, douban_id, image, title, alt, author, publisher, tags, summary]
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
    # 将 book_details_dict 的 values 按一定顺序取出放入 list

    keywords = [
        'isbn',
        'douban_id',
        'image',
        'title',
        'alt',
        'author',
        'publisher',
        'tags',
        'summary'
    ]
    book_details_list = []
    for k in keywords:
        book_details_list.append(book_details_dict[k])

    # 添加一条记录
    sql_insert = """
        INSERT INTO book_details(isbn, douban_id, image, title, alt, author, publisher, tags, summary) 
        VALUES(?,?,?,?,?,?,?,?,?)
    """

    try:
        sqlite_cursor.execute(sql_insert, tuple(book_details_list))
        conn.commit()
        return 1

    except sqlite3.IntegrityError:
        print("添加书籍详情到数据库失败，原因: 该条数据已经在数据库中")
        return 2

    except sqlite3.Error as e:
        print("添加书籍详情失败！原因: " + "\n" + e.args[0])
        return 0


def book_crawler(isbn=None):
    import requests
    url = 'https://api.douban.com/v2/book/isbn/'+isbn
    param = 'id,isbn13,title,alt,image,author,publisher,tags,summary'
    dt = requests.get(url, params={'fields':param}).json()
    try:
        book_details = dict(
            isbn=dt['isbn13'],
            douban_id=dt['id'],
            image=dt['image'],
            title=dt['title'],
            publisher=dt['publisher'],
            author=dt['author'][0],
            summary=dt['summary'],
            alt=dt['alt'],
            tags=dt['tags'][0]['name']
        )
        return book_details

    except KeyError:
        return None

class current_user():
    """未加入 flask_login 模块前开发测试用，获得当前登录用户的id"""
    @classmethod
    def get_id(cls):
        return 1

def test_crwaler(isbn=None):
    dic = book_crawler(isbn=isbn)
    try:
        print('豆瓣id', dic['id'])
        print('isbn', dic['isbn13'])
        print('书名', dic['title'])
        print('豆瓣网址', dic['alt'])
        print('中号图片', dic['image'])
        print('作者', dic['author'][0])
        print('出版社', dic['publisher'])
        print('类目', dic['tags'])
        print('简介', dic['summary'])
    except KeyError:
        dic = '抱歉，豆瓣还没有您这本书的信息。请您先将这部书的信息上传至豆瓣网，谢谢！'
        print(dic)

def test_insert(db):
    user_info_dt = dict(
        username='test@name.com',
        password_hash='123456',
        nickname='test',
        wechat='test',
        location='cq',
    )
    for i in range(5):
        user_id = 2
        isbn = 200+i
        title = 'title %s' % isbn
        book_list_dt = dict(
            isbn=isbn,
            state=1,
            user_id=user_id,
        )
        book_details_dt = dict(
            isbn=isbn,
            douban_id=663,
            image='image_url',
            title=title,
            alt='alt',
            author='author',
            publisher='publisher',
            tags='tags',
            summary='summary',
        )

        user_xiami = User(**user_info_dt)
        book_list = BookList(**book_list_dt)
        book_details = BookDetails(**book_details_dt)

        # db.session.add_all([user_xiami, book_list, book_details])
        db.session.add_all([book_list, book_details])

    db.session.commit()


if __name__ == '__main__':

    # r = cursor.fetchall()
    # r = get_user_books(user_id=3)
    # r = get_book_details(local_id=1)
    # r = book_crawler(isbn='9787508680231')
    # print('r:',r)
    # re = insert_book_details(r)
    # print('re', re)
    r = get_books_list(title="裂")
    import json
    print('r:', json.dumps(r, indent=2, ensure_ascii=False))

