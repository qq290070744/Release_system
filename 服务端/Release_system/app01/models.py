from django.db import models
from django.contrib.auth.models import User as sysusers


# Create your models here.


class User(models.Model):
    username = models.CharField(u'用户名', max_length=30)
    headImg = models.FileField(u'文件名', upload_to='static/upload/')
    service_type = models.CharField(u'服务类型', max_length=30, null=True)
    updatetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "用户：{}，文件名：{}".format(self.username, self.headImg)


class userpro(models.Model):
    user = models.OneToOneField(sysusers)
    name = models.CharField(u'姓名', max_length=30)

    def __str__(self):
        return "用户姓名：%s,用户名：%s" % (self.name, self.user)


class his_rel(models.Model):
    host = models.CharField(u'主机', max_length=30, null=True)
    host_group = models.CharField(u'主机组', max_length=30, null=True)
    filename = models.CharField(u'文件名', max_length=30)
    service_type = models.CharField(u'服务类型', max_length=30)
    status = models.IntegerField(u'发布状态')
    relea_time = models.DateTimeField(u'发布时间', auto_now=True)

    def __str__(self):
        return "主机：{}，              主机组：{}，              文件名：{}，                服务类型：{}，                发布状态：{}，                    发布时间：{}".format(
            self.host, self.host_group, self.filename,
            self.service_type, self.status,
            self.relea_time)


class host_list(models.Model):
    hostname = models.CharField(u'主机名', max_length=30)
    ip = models.CharField(u'主机ip', max_length=30)
    host_group = models.CharField(u'主机组', max_length=30)
    updatetime = models.DateTimeField(u'添加时间', auto_now=True, null=True)

    def __str__(self):
        return "主机名:{} ,主机ip:{} ,主机组:{} ,添加时间:{}".format(self.hostname, self.ip, self.host_group, self.updatetime)


class service_type(models.Model):
    service_name = models.CharField(u'服务名称,如:apache', max_length=30)
    service_processname = models.CharField(u'服务进程名称,如httpd', max_length=30, null=True)
    demo_path = models.CharField(u'代码所在路径,软连接要链到的地方,如/var/www/html', max_length=90, null=True)
    install_type = models.CharField(u'软件安装方式(yum rpm/make 源码编译)', max_length=30)
    updatetime = models.DateTimeField(u'添加时间', auto_now=True, null=True)

    def __str__(self):
        return self.service_name


class server_ip_and_port(models.Model):
    server_ip = models.CharField(u'服务端ip地址', max_length=30)
    server_port = models.CharField(u'服务端port,\n是访问django的端口', max_length=30)

    def __str__(self):
        return "{}:{}".format(self.server_ip, self.server_port)


class his_rool(models.Model):
    host = models.CharField(u'主机', max_length=30, null=True)
    host_group = models.CharField(u'主机组', max_length=30, null=True)
    filename = models.CharField(u'文件名', max_length=30)
    service_type = models.CharField(u'服务类型', max_length=30)
    status = models.IntegerField(u'状态')
    relea_time = models.DateTimeField(u'回滚时间', auto_now=True)

    def __str__(self):
        return "主机：{}，              主机组：{}，              文件名：{}，                服务类型：{}，                发布状态：{}，                    回滚时间：{}".format(
            self.host, self.host_group, self.filename,
            self.service_type, self.status,
            self.relea_time)
