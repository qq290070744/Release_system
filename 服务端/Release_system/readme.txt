����ͻ���Ҫִ�е�����
yum -y install epel-release
yum -y install python-pip

pip install --upgrade pip
pip install pymysql
pip install requests
pip install django

cd �ͻ���·��
python manage.py runserver 0.0.0.0:9999
