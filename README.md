部署客户端要执行的命令
yum -y install epel-release
yum -y install python-pip

pip install --upgrade pip
pip install pymysql
pip install requests
pip install django

cd 客户端路径
python manage.py runserver 0.0.0.0:9999
