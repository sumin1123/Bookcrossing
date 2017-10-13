# coding:utf-8

"""
目前需要 4 个函数
其功能，传入参数和返回值，返回值的格式都在 docstring 中写出
"""


def get_user_books(users_id=None):
    """
    根据 users_id 得到用户所有已发布的书的信息

    Args:
        users_id(int): 用户id

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
    """
    pass


def get_books_detail(local_id=None):
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

    pass


def get_books_list(isbn=None, title=None):
    """
    用户输入 isbn 或者 title 检索数据库内是否有相关书籍
    根据 isbn 或者 title 检索，每次检索的条件只有一个，其中
        isbn 全部匹配
        title 模糊查找，部分匹配即可。如果实现困难则改为全部匹配

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


def delete_book(users_id=None, local_id=None):
    """
    用户删除已发布的书

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