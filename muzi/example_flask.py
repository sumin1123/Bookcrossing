from flask import Flask, request, render_template, flash, session, redirect, url_for
from database_test.dbApi import insert_user_info, get_user_info# 导入数据库函数
from database_test.dbInit import db_init# 导入数据库函数
# from database_test import dbApi, dbInit
import os
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

# user models
class User(UserMixin):
    pass

app = Flask(__name__)
login_manager = LoginManager(app)

secret_key_gen = os.urandom(24)
app.secret_key = secret_key_gen # 产生随机key

# 指定登录界面视图函数
login_manager.login_view = 'index'
#能够更好的防止恶意用户篡改 cookies, 当发现 cookies 被篡改时, 该用户的 session 对象会被立即删除, 导致强制重新登录. 
login_manager.session_protection = "strong"
#指定了提供用户登录的文信息
login_manager.login_message = "请在此页面登录"
#指定了登录信息的类别为 info 
login_manager.login_message_category = "info"

# 加载index.html
@app.route("/")
def index():
    return render_template("index.html")

"""
功能：
1.  在注册页面获取用户注册信息，注册信息包括：用户名、密码、昵称、微信号、位置
用户密码需要长度大于8。
2. 填写完注册信息后，点击提交按钮，将会自动跳转到登录界面。
3. 点击登录按钮，也会跳转到登录界面。
"""
@app.route('/register', methods = ["POST","GET"])
def register():
    user_data = {'user_name': "", 'password': "", 'nickname': "", 'wechat': "", 'location': ""}
    if request.method == 'POST':
        user_data['user_name']  = request.form.get("user_name", None)     #用户名
        user_data['password']  = request.form.get("password", None)         # 密码
        user_data['nickname'] = request.form.get("nickname", None)            #昵称
        user_data['wechat'] = request.form.get("wechat", None)                    #微信号
        user_data['location'] = request.form.get("location", None)                  #位置
        if request.form.get("agreement"):
            #if query_user_register(user_data['user_name'], user_data_que):
            a = get_user_info(user_data['user_name'])
            if a is not None:
                flash("用户名已被占用")
            elif len(user_data['user_name']) == 0 or len(user_data['password']) == 0:
                flash('密码或用户名为空')
            else:
                if len(user_data['password']) <= 8:
                    flash('密码过短，密码长度需要大于8个字母')
                else:
                    secret = generate_password_hash(user_data['password']) #对密码进行加密
                    user_data['password'] = secret
                    insert_user_info(user_data)
                    return redirect(url_for('login'))
        else:
             flash('请勾选确认框')
    else:
        if request.args.get("action")== u'登录':
            return redirect(url_for('login'))
        else:
            return render_template("register.html")
    return render_template("register.html")


"""
将登陆的用户名存入session中
"""
@login_manager.user_loader
def load_user(user_id):
    if get_user_info(user_id) is not None:
        curr_user = User()
        curr_user.id = user_id
        return curr_user

"""
功能：
   1.  在登录界面点击登录按钮，会自动跳转进入my_books界面
   2.  在登录界面点击注册按钮，会自动跳转到注册界面
"""
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get('user_name')
        user = get_user_info(user_name)
        try:
            username_from_db = user[1]
            userpassword_from_db = user[2]
        except TypeError:
            flash("该用户没有注册，请先注册")
            return render_template("log_in.html")
        else:
            check_password = check_password_hash(userpassword_from_db, request.form.get('password')) #对密码进行解密
            # if username_from_db is not None and userpassword_from_db == request.form.get('password'):
            if username_from_db is not None and check_password:
                curr_user = User()
                curr_user.id = user_name
                login_user(curr_user, remember = request.form.get('remember'))
                next = request.args.get('next')
                return redirect(next or url_for('my_books'))
            else:
                flash("用户不存在或密码错误",'warning')
                return render_template("log_in.html")           
        render_template("log_in.html")
    return render_template("log_in.html")

"""
点击my_books界面的登出按钮会直接登出，跳转到index界面
"""
@app.route('/my_books')
@login_required
def my_books():
    return render_template("my_books.html")

"""
登出，从session中删除用户信息
"""
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db_init()
    app.run(debug=True)  
