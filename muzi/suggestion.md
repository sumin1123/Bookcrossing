#### 对前端的建议：
1. 在一个.html文件中，关联信息使用一个表单(form)，例如在register.html中，可以将用户名、密码、昵称、微信号、所在城市，以及提交按钮放在一个表单，然后将登陆放在另一个表单。
这样执行提交或者登陆时会跳转不同url，同时可以获取到对应表单中的信息；
2. 需要增加一个注册成功.html，注册成功后会跳转
3. 某些html中的按钮可以去掉：
  - log_in.html中不需要登录按钮，因为已经存在一个登入；
  - register.html中不需要注册按钮，因为已经在注册页面，不需要该按钮；
  - 在log_in.html中按钮的name修改为action，因为点击不同按钮会跳转到不同url，我使用if..elif..else语句对命令进行判断；
  - register.html中同上；
5. 建议添加一条语句防止.ico 404错误
6. form表单需要提供action地址：例如<form action = "login_success">  </form> 
> <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">


#### 对数据的建议：
1. 我会将获得的注册信息传递给数据库；
2. 我需要数据库根据数据的用户名返回注册时的密码；
3. 函数的具体设计见muzi目录下[demand.py](https://github.com/sumin1123/Bookcrossing/blob/develop/muzi/demand.py)文件。


#### 注册登录demo
在muzi文件夹下面有我写的一个注册登录的mvp程序。根据上述的意见，在templates中对原有log_in.html，register.html，index.html进行了修改。