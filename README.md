服务端在3.5下跑
客户端在2.7下跑

部署客户端要执行的命令
yum -y install epel-release

yum -y install python-pip

pip install --upgrade pip

pip install pymysql

pip install requests

pip install django

cd 客户端路径
python manage.py runserver 0.0.0.0:9999

![Alt text](http://121.201.68.21:8080/static/release/1.png)
![Alt text](http://121.201.68.21:8080/static/release/2.png)
![Alt text](http://121.201.68.21:8080/static/release/3.png)
![Alt text](http://121.201.68.21:8080/static/release/4.png)
![Alt text](http://s1.51cto.com/images/20180504/1525403548451542.png)
