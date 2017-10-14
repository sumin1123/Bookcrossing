from flask import Flask, request, render_template, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'  

class value_user(object):
    details_check_in = {}
    details_check_out = {}
    check_in = []
    check_out = []

value_user_inst = value_user()

@app.route('/', methods=["GET"])
def base():
  return render_template("index.html") 

@app.route('/login', methods = ["GET"])
def login():
    return render_template("log_in.html")

@app.route('/login_success', methods = ["GET"])
def login_success():
    user_name  = request.args.get("user_name")
    password  = request.args.get("password")
    print("this is check_in: ", value_user_inst.check_in)
    print("this is check_out: ", value_user_inst.check_out)
    print("this is details_check_in: ", value_user_inst.details_check_in)
    print("this is details_check_out: ", value_user_inst.details_check_out)
    cmd  = request.args.get("action") # value  = 登入, value = 注册
    if cmd == u'登入':
        if len(user_name) == 0 or len(password) == 0:
            #提示信息 密码或用户名为空
            return render_template('help.html')
        else:
            #if personal_details_check_out.get(user_name) == password:
            abcvd = value_user_inst.details_check_in.get(user_name)
            if password in value_user_inst.details_check_in.get(user_name)  :           
                return render_template("success.html")
            else:
                #提示信息 密码或用户名不正确
                return render_template('help.html')
    elif cmd == u'注册':
        return render_template("register.html")
    else: 
        return render_template("log_in.html")

@app.route('/register', methods = ['GET'])
def register():
    return render_template("register.html")

@app.route("/register_submit", methods = ["GET" or "POST"])
def registerpost():
    user_name  = request.args.get("user_name")
    password  = request.args.get("password")
    nickname = request.args.get("nickname")
    wechat = request.args.get("wechat")
    location = request.args.get("location")
    agreement = request.args.get("agreement")  # value = agree
    cmd  = request.args.get("action") # value = 提交 , value = 注册 , value = 登录

    value_user_inst.details_check_out[user_name] = [password, nickname, wechat, location]
    value_user_inst.check_out = [user_name, password, nickname, wechat, location]

    if cmd == u'提交':
        if agreement == 'agree':
            if len(user_name) == 0 or len(password) == 0:
                #提示信息 密码或用户名为空
                return render_template("help.html")
            else:
                if len(password) <= 8:
                    #提示信息，密码过短
                    return render_template("register.html")
                else:
                    value_user_inst.details_check_in[user_name] = [password, nickname, wechat, location]
                    value_user_inst.check_in = [user_name, password, nickname, wechat, location]
                    return render_template("log_in.html")
        else:
            #信息提示，请勾选确认
            return render_template("register.html")
    elif cmd == u'登录':
        return render_template("log_in.html")
    else:
        return render_template("register.html")




if __name__ == '__main__':
    app.run(debug=True)  