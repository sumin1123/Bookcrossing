#! python3

from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
@app.route('/')
def index():
    if request.args.get('release_books') == '发布书':
        return redirect('/release')
    if request.args.get('help') == '帮助':
        help_file = 'smpb'
        return render_template('help.html', help_file=help_file)
    if request.args.get('modify_information') == '修改个人信息':
        user_name = 'sumin@sina.com'
        password = '********'
        nickname = 'sm'
        wechat = 'niaow-sauce'
        location = 'beijing'
        return render_template('change.html', user_name=user_name, password=password,
                               nickname=nickname, wechat=wechat, location=location)
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    return render_template('search_books.html', list=list)
@app.route('/my')
def my():
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if request.args.get('help') == '帮助':
        help_file = 'ok'
        return render_template('help.html', help_file=help_file)
    return render_template('my_books.html', list=list)
@app.route('/details/<name>')
def details(name):
    nickname = 'sm'
    location = 'beijing'
    wechat = 'miaow-sauce'
    title = '目送'
    author = '龙应台'
    publisher = '三联出版社'
    isbn = '9787108032911'
    alt = 'https://book.douban.com/e26/'
    summary = '这是龙应台的简介这是龙应台的简介这是龙应台的简介这是龙应台的简介这是龙应台的简介这是龙应台的简介'
    return render_template('details.html', nickname=nickname, location=location, wechat=wechat,
                           title=title, author=author, publisher=publisher, isbn=isbn, alt=alt,
                           summary=summary)
@app.route('/release')
def release():
    release_information = '请在这里输入书籍的ISBN号码，不含"_"，系统将向豆瓣请求数据。'
    nickname = 'sm'
    location = 'beijing'
    wechat = 'miaow-sauce'
    title = '目送'
    author = '龙应台'
    publisher = '三联出版社'
    isbn = '9787108032911'
    alt = 'https://book.douban.com/e26/'
    return render_template('release_books.html', nickname=nickname, location=location, wechat=wechat,
                           title=title, author=author, publisher=publisher, isbn=isbn, alt=alt,
                           release_information=release_information)



if __name__ == '__main__':
    app.run()
