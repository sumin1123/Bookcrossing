~这里存放用户注册、登陆相关模块的脚本文件，由木子开发维护
1. 直接运行muzi目录下面的example_flask.py文件，可以测试注册和登录功能。
2. 在example_flask.py文件中，使用绝对路径导入数据库函数，相对路径导入多次失败，按照网上的方法还未解决，因此采用绝对路径导入
> from database_test.dbInit import db_init
3. 修改了传入数据库的接口，自行修改dbApi中insert_user_info函数的部分内容，修改如下
```
    # 取出输入的字典参数值
    # for k, v in user_check_in.items():
    #     userName = k
    #     userInfo = v
    # user_name = userName
    # password, nickname, wechat_id, location = userInfo[0], userInfo[1], userInfo[2], userInfo[3]
    user_name = user_check_in.get('user_name')
    password = user_check_in.get('password')
    nickname = user_check_in.get('nickname')
    wechat_id = user_check_in.get('wechat')
    location = user_check_in.get('location')
```

4. 使用LoginManager模块，使用@login_required装饰器限制非登录用户浏览的界面。例如只有登录用户能够进入my_books.html，未登录用户如果输入http://127.0.0.1:5000/my_books，会自动转入登录界面
```
@app.route('/my_books')
@login_required
def my_books():
    return render_template("my_books.html")
```

5. 将templeates文件夹的内容复制到muzi文件下进行修改，修改的地方如下：
  - 在register.html和log_in.html中增加，页面信息提示功能，代码如下
  ```
{% for messages in get_flashed_messages() %}
    <div>{{ messages}}</div>
{% endfor %}
    ```
 - 将my_books.html中登出按钮的连接关联至/logout
 > action="/logout"




问题：
muzi/
        __init__.py

        database_test/
           
                __init__.py

                dbApi.py

                dbInit.py

        templates/

        example_flask.py

在example_flask.py中调用database_test文件夹下dbApi.py文件中的insert_user_info函数
如果使用相对路径的方法导入，from .database_test.dbApi import insert_user_info
出现错误：ModuleNotFoundError: No module named '__main__.database_test'; '__main__' is not a package
如果使用绝对路径的方法导入没有报错
from .database_test.dbApi import insert_user_info

查看了文档[PEP 328 -- Imports: Multi-Line and Absolute/Relative](https://www.python.org/dev/peps/pep-0328/#rationale-for-relative-imports)还是没有找到解决的方法
