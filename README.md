# Bookcrossing
# Feature
- 用户注册登录
- 发布闲置书籍
- 浏览和搜索他人已发布的书籍

# Requirements
- Python 3.6.2
- 依赖包：见 `requirements.txt` 

# Installation
1.	将本仓库 clone 至本地
2.	安装所需依赖包，推荐创建一个虚拟环境，在该虚拟环境下进入仓库根目录 `requirements.txt` 
		
	```
	pip install -r requirements.txt
	```
	
# Usage
1.	进入虚拟环境，然后初始化数据库

	```
	(venv) $ python manage.py shell 
	>>> db.create_all()
	>>> exit()
	```
	
2.	设置邮箱功能相关参数
	因为在用户注册，修改密码等环节时，服务端会向注册用户发送邮件，这时就需要使用一个邮箱来发送对应的邮件。需要设置邮箱的**SMTP服务器地址**，**SSL协议端口**，**SMTP 认证账户名**，**SMTP 认证授权码**
	- **SMTP服务器地址**和**SSL协议端口参数**在 `config.py` 内进行设置和修改。参数值可参见邮箱服务商的相关说明，默认使用的是163邮箱，相关参数可见：[163邮箱的SMTP设置帮助](http://help.mail.163.com/faqDetail.do?code=d7a5dc8471cd0c0e8b4b8f4f8e49998b374173cfe9171305fa1ce630d7f67ac22dc0e9af8168582a)
		`config.py` 文件内相关部分为：
		```python
		class Config:
		    ...
		    MAIL_USE_SSL = True  # 使用 SSL 协议传输
		    MAIL_SERVER = 'smtp.163.com'
		    MAIL_PORT = 994  # 163 的 SSL 协议端口号
		    
		    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # 邮箱的 SMTP 认证账户名，163邮箱为邮箱账号,如 xx@163.com，需要在环境变量中设置
		    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # 邮箱的 SMTP 认证授权码，需要在环境变量中设置	
		```
	- **SMTP 认证账户名**，**SMTP 认证授权码** 在环境变量中设置
		- Windows 
		
		```
		(venv) $ set MAIL_USERNAME=xx@163.com # 邮箱地址
		(venv) $ set MAIL_PASSWORD=xxxxx  # 邮箱客户端 SMTP 认证授权码（不同于登录的密码）
		```
		- Linux/MacOsX 
		
		```
		(venv) $ export MAIL_USERNAME='xx@163.com' # 邮箱地址
		(venv) $ export MAIL_PASSWORD='xxxxx'  # 邮箱客户端 SMTP 认证授权码（不同于登录的密码）
		```
3. 启动服务端
	2.1 测试
	以带参数方式启动服务器，指定运行的端口和服务端监听的 ip 地址
	```
	(venv) $ python manage.py runserver --host 0.0.0.0 -p 3000
	```
	2.2 上线
	需要使用 `gunicorn` ，在之前安装依赖包过程中，`gunicorn` 已安装，使用下述命令启动服务端
	```
	(venv) $ gunicorn manage:app  --bind 0.0.0.0:3000
	```

# Changelog

- V1.0
	- Feature
		- 实现用户注册，修改邮箱等用户相关的功能模块
		- 实现发布书，搜索书的相关模块



