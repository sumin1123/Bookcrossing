#! python3
# coding: utf-8

import requests
import io
import sys
import json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

def books(isbn):
    url = 'https://api.douban.com/v2/book/isbn/'+isbn
    #param = 'id,isbn13,title,alt,image,author,publisher,tags,summary'
    #dic_def = requests.get(url, params={'fields':param}).json()
    dic_def = requests.get(url).json()
    return dic_def

if __name__ == "__main__":
    while True:
        book_isbn = input('>')
        dic = books(book_isbn)
        try:
            print('豆瓣id', dic['id'])
            print('isbn', dic['isbn13'])
            print('书名', dic['title'])
            print('豆瓣网址', dic['alt'])
            print('中号图片', dic['image'])
            print('作者', dic['author'])
            print('出版社', dic['publisher'])
            print('类目', dic['tags'])
            print('简介', dic['summary'])
            print(dic)
        except KeyError:
            dic = '抱歉，豆瓣还没有您这本书的信息。请您先将这部书的信息上传至豆瓣网，谢谢！'
            print(dic)
