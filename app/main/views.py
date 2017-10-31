from flask import render_template, request
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import main
from .forms import Isbn
from .douban import books
from .. import db
from ..models import User, Detail, Book, Mail
import json
from datetime import *
#import requests
#import io
#import sys
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

#def book(isbn):
#    url = 'https://api.douban.com/v2/book/isbn/'+isbn
#    #param = 'id,isbn13,title,alt,image,author,publisher,tags,summary'
#    #dic_def = requests.get(url, params={'fields':param}).json()
#    dic_def = requests.get(url).json()
#    return dic_def

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/introduction')
def introduction():
    return render_template('introduction.html')

@main.route('/browse', methods=['GET', 'POST'])
def browse():
    list = []
    for i in Book.query.all():
        isb = i.isbn
        bk_id = i.id
        det = Detail.query.filter_by(isbn=isb).first()
        tit = det.title
        ima = det.image
        dab = [ima, tit, bk_id]
        list.append(dab)
    if request.args.get('find') == 'Find':
        try:
            t = request.args.get('title_s')
            try:
                if int(t) >= 1000000000000 and int(t) <= 9999999999999:
                    list_i = []
                    j = Book.query.filter_by(isbn=int(t)).first()
                    if j == None:
                        alert = '没有您所搜的这本书！'
                        return render_template('browse.html', alert=alert)
                    else:
                        for j in Book.query.filter_by(isbn=int(t)).all():
                            isb = j.isbn
                            bk_id = j.id
                            det = Detail.query.filter_by(isbn=isb).first()
                            tit = det.title
                            ima = det.image
                            dab = [ima, tit, bk_id]
                            list_i.append(dab)
                    return render_template('browse.html', list=list_i)
            except ValueError:
                if t == '':
                    list_n = []
                    for i in Book.query.all():
                        isb = i.isbn
                        bk_id = i.id
                        det = Detail.query.filter_by(isbn=isb).first()
                        tit = det.title
                        ima = det.image
                        dab = [ima, tit, bk_id]
                        list_n.append(dab)
                    return render_template('browse.html', list=list_n)
                tit_s = Detail.query.filter(Detail.title.like("%"+t+"%")).all()
                #print(tit_s)
                list_s = []
                for k in tit_s:
                    isb_s = k.isbn
                #    print(isb_s)
                    for j in Book.query.filter_by(isbn=isb_s).all():
                        isb = j.isbn
                        bk_id = j.id
                        det = Detail.query.filter_by(isbn=isb).first()
                        tit = det.title
                        ima = det.image
                        dab = [ima, tit, bk_id]
                        list_s.append(dab)
                return render_template('browse.html', list=list_s)
        except AttributeError:
            alert = '没有您所搜的这本书！'
            return render_template('browse.html', alert=alert)

    return render_template('browse.html', list=list)

@main.route('/release', methods=['GET', 'POST'])
def release():
    #form = Isbn()
    if request.args.get('search') == 'Search':
        book_isbn = request.args.get('isbn')
        dic = books(book_isbn)
        try:
            ima = dic['images']['large']
            tit = dic['title']
            aut = dic['author'][0]
            pub = dic['publisher']
            isb = book_isbn
            al = dic['alt']
            summ = dic['summary']
            username = current_user.username
            location = current_user.location
            wechat = current_user.wechat
            if Detail.query.filter_by(isbn=book_isbn).first():
                pass
            else:
                detail = Detail(isbn=book_isbn,
                                douban_id=dic['id'],
                                image=dic['image'],
                                image_l=ima,
                                title=tit,
                                alt=al,
                                author=aut,
                                publisher=pub,

                                summary=summ
                                )
                                #author=aut,
                                #tags=dic['tags'],
                db.session.add(detail)
            book = Book(isbn=book_isbn,
                        user_id=current_user.id)
            db.session.add(book)
            db.session.commit()
            #if request.args.get('release') == 'Release':


            return render_template('release.html',
                                   image=ima,
                                   title=tit,
                                   author=aut,
                                   publisher=pub,
                                   isbns=isb,
                                   alt=al,
                                   summary=summ,
                                   username=username,
                                   location=location,
                                   wechat=wechat,
                                   )


        except KeyError:
            alert = '抱歉，豆瓣还没有您这本书的信息。请您先将这部书的信息上传至豆瓣网，谢谢！'
            return render_template('release.html', alert=alert)


    return render_template('release.html')

@main.route('/mybooks', methods=['GET', 'POST'])
def mybooks():
    if current_user.is_authenticated:
        list = []
        for i in Book.query.filter_by(user_id=current_user.id).all():
            isb = i.isbn
            bk_id = i.id
            det = Detail.query.filter_by(isbn=isb).first()
            tit = det.title
            ima = det.image
            dab = [ima, tit, bk_id]
            list.append(dab)

        if request.args.get('find_my') == 'Find_my':
            try:
                t = request.args.get('title_my')
                try:
                    if int(t) >= 1000000000000 and int(t) <= 9999999999999:
                        list_i = []
                        j = Book.query.filter_by(isbn=int(t)).first()
                        if j == None:
                            alert = '没有您所搜的这本书！'
                            return render_template('browse.html', alert=alert)
                        else:
                            for j in Book.query.filter_by(isbn=int(t)).all():
                                if j.user_id == current_user.id:
                                    isb = j.isbn
                                    bk_id = j.id
                                    det = Detail.query.filter_by(isbn=isb).first()
                                    tit = det.title
                                    ima = det.image
                                    dab = [ima, tit, bk_id]
                                    list_i.append(dab)
                        return render_template('browse.html', list=list_i)

                except ValueError:
                    if t == '':
                        list_n = []
                        for i in Book.query.filter_by(user_id=current_user.id).all():
                            isb = i.isbn
                            bk_id = i.id
                            det = Detail.query.filter_by(isbn=isb).first()
                            tit = det.title
                            ima = det.image
                            dab = [ima, tit, bk_id]
                            list_n.append(dab)
                        return render_template('mybooks.html', list=list_n)
                    tit_s = Detail.query.filter(Detail.title.like("%"+t+"%")).all()
                    #print(tit_s)
                    list_s = []
                    for k in tit_s:
                        isb_s = k.isbn
                    #    print(isb_s)
                        for j in Book.query.filter_by(isbn=isb_s).all():
                            if j.user_id == current_user.id:
                                isb = j.isbn
                                bk_id = j.id
                                det = Detail.query.filter_by(isbn=isb).first()
                                tit = det.title
                                ima = det.image
                                dab = [ima, tit, bk_id]
                                list_s.append(dab)
                    return render_template('mybooks.html', list=list_s)
            except AttributeError:
                alert = '没有您所搜的这本书！'
                return render_template('mybooks.html', alert=alert)

        dele = request.args.get('dele')
        if dele == None:
            pass
        else:
            try:
                book_d = Book.query.filter_by(id=dele).first()
                db.session.delete(book_d)
                db.session.commit()
                list_r=[]
                for i in Book.query.filter_by(user_id=current_user.id).all():
                    isb = i.isbn
                    bk_id = i.id
                    det = Detail.query.filter_by(isbn=isb).first()
                    tit = det.title
                    ima = det.image
                    dab = [ima, tit, bk_id]
                    list_r.append(dab)
                return render_template('mybooks.html', list=list_r)
            except:
                pass
        #for i in range(1000):
        #    if request.args.get('d%d'% (i)) == 'D%d'% (i):
        #        print(i)
        return render_template('mybooks.html', list=list)
    return render_template('mybooks.html')

@main.route('/detail/<name>')
def detail(name):
    det = Book.query.filter_by(id=name).first()
    isb = det.isbn
    det_d = Detail.query.filter_by(isbn=isb).first()
    image = det_d.image_l
    title = det_d.title
    author = det_d.author
    publisher = det_d.publisher
    isbn = det_d.isbn
    alt = det_d.alt
    summary = det_d.summary
    use_id = det.user_id
    use = User.query.filter_by(id=use_id).first()
    username = use.username
    location = use.location
    wechat = use.wechat
    id = use.id
    return render_template('detail.html', image=image,
                                          title=title,
                                          author=author,
                                          publisher=publisher,
                                          isbns=isbn,
                                          alt=alt,
                                          summary=summary,
                                          username=username,
                                          location=location,
                                          wechat=wechat,
                                          id=id)

@main.route('/friendbooks/<user>')
def friendbooks(user):
    if current_user.is_authenticated:
        list = []
        x = User.query.filter_by(id=user).first()
        user_n = x.username
        user_id = user
        for i in Book.query.filter_by(user_id=user).all():
            isb = i.isbn
            bk_id = i.id
            det = Detail.query.filter_by(isbn=isb).first()
            tit = det.title
            ima = det.image
            dab = [ima, tit, bk_id]
            list.append(dab)

        if request.args.get('find_friend') == 'Find_friend':
            try:
                t = request.args.get('title_friend')
                try:
                    if int(t) >= 1000000000000 and int(t) <= 9999999999999:
                        list_i = []
                        j = Book.query.filter_by(isbn=int(t)).first()
                        if j == None:
                            alert = '没有您所搜的这本书！'
                            return render_template('friendbooks.html', alert=alert, id=user_id)
                        else:
                            for j in Book.query.filter_by(isbn=int(t)).all():
                                if j.user_id == int(user):
                                    isb = j.isbn
                                    bk_id = j.id
                                    det = Detail.query.filter_by(isbn=isb).first()
                                    tit = det.title
                                    ima = det.image
                                    dab = [ima, tit, bk_id]
                                    list_i.append(dab)
                        return render_template('friendbooks.html', list=list_i, id=user_id)

                except ValueError:
                    if t == '':
                        list_n = []
                        for i in Book.query.filter_by(user_id=user).all():
                            isb = i.isbn
                            bk_id = i.id
                            det = Detail.query.filter_by(isbn=isb).first()
                            tit = det.title
                            ima = det.image
                            dab = [ima, tit, bk_id]
                            list_n.append(dab)
                        return render_template('friendbooks.html', list=list_n, id=user_id)
                    tit_s = Detail.query.filter(Detail.title.like("%"+t+"%")).all()
                    #print(tit_s)
                    list_s = []
                    for k in tit_s:
                        isb_s = k.isbn
                    #    print(isb_s)
                        for j in Book.query.filter_by(isbn=isb_s).all():
                            if j.user_id == int(user):
                                isb = j.isbn
                                bk_id = j.id
                                det = Detail.query.filter_by(isbn=isb).first()
                                tit = det.title
                                ima = det.image
                                dab = [ima, tit, bk_id]
                                list_s.append(dab)
                    return render_template('friendbooks.html', list=list_s, id=user_id)
            except AttributeError:
                alert = '没有您所搜的这本书！'
                return render_template('friendbooks.html', alert=alert, id=user_id)

    return render_template('friendbooks.html', list=list, user_n=user_n, id=user_id)

@main.route('/friendlocation/<loca>')
def firendlocation(loca):
    location = loca
    list_f = []
    for i in User.query.filter_by(location=loca).all():
        user_id = i.id
        user_name = i.username
        dab = [user_id, user_name]
        list_f.append(dab)
    return render_template('friendlocation.html', location=location, list_f=list_f)

@main.route('/location')
def location():
    list_lo = []
    for i in User.query.all():
        user_loc = i.location
        if user_loc in list_lo:
            pass
        else:
            list_lo.append(user_loc)

    return render_template('location.html', list_lo=list_lo)

@main.route('/mail/<u_id>')
def mail(u_id):
    na = User.query.filter_by(id=u_id).first()
    user_na = na.username
    if request.args.get('send_mail') == 'Send_mail':
        body = request.args.get('textarea')
        if body == '':
            return render_template('mail.html', user_na=user_na)
        t = datetime.now()
        time = t.strftime( '%y-%m-%d %I:%M:%S %p' )
        mail = Mail(body=body,
                    send=current_user.id,
                    receive=u_id,
                    time=time,
                    )
        db.session.add(mail)
        db.session.commit()
        return render_template('mail.html', user_na=user_na)
    return render_template('mail.html', user_na=user_na)

@main.route('/mymails')
def mymails():
    list_u = []
    for i in Mail.query.filter_by(receive=current_user.id).all():
        sen = i.send
        us = User.query.filter_by(id=i.send).first()
        use = us.username
        bod = i.body
        tim = i.time
        dab = [use, bod, tim, sen]
        list_u.append(dab)
    return render_template('mymails.html', list_u=list_u)

@main.route('/details')
def details():
    return render_template('details.html')
