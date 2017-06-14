#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#from __future__ import unicode_literals

from django.db import models

# Create your models here.
class his_rel(models.Model):
    host=models.CharField(max_length=30)
    filename=models.CharField(max_length=30)
    service_type=models.CharField(max_length=30)
    status=models.IntegerField()
    relea_time=models.DateTimeField(auto_now=True)

class service_type(models.Model):
    service_name = models.CharField(u'服务名称', max_length=30)
    service_processname = models.CharField(u'服务进程名称', max_length=30)
    demo_path=models.CharField(u'代码所在路径,,软连接要链到的地方,如/var/www/html', max_length=90,null=True)
    install_type = models.CharField(u'软件安装方式(yum rpm/make 源码编译)', max_length=30)
    updatetime = models.DateTimeField(u'添加时间', auto_now=True, null=True)

class server_ip_and_port(models.Model):
    server_ip=models.CharField(u'服务端ip地址', max_length=30)
    server_port = models.CharField(u'服务端port', max_length=30)
    def __unicode__(self):
        return "{}:{}".format(self.server_ip,self.server_port)

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