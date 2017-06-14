# coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import requests, json, os, shutil, time, zipfile, tarfile
from  app01.models import *
from  app01.models import service_type as servicetype

ip_port = server_ip_and_port.objects.all()
for i in ip_port:
    serverip = i.server_ip
    serverport = i.server_port

# demo_path = service_type.objects.all()
# for i in demo_path:
#     if i.service_name == "apache":
#         apache_path = i.demo_path
#     if i.service_name == "nginx":
#         nginx_path = i.demo_path


@csrf_exempt
def get_cmd(request):
    if request.method == "POST":
        print(request.POST)
        host = request.POST['host']
        filename = request.POST['file']
        dirname = request.POST['dir']
        service_type = request.POST['service_type']
        urlfile = "http://%s:%s/static/upload/%s" % (serverip, serverport, filename)
        print(urlfile, dirname, service_type)
        downloadImageFile(urlfile, dirname)
        if exec_rele(service_type, filename, dirname):
            # relea_time__gte=time.strftime("%Y-%m-%d")
            his_rel.objects.filter(status=1,
                                   host=host,
                                   filename=filename,
                                   relea_time__gte=time.strftime("%Y-%m-%d"),
                                   relea_time=request.POST['time']).update(status=2)
            print("----------------------update status ok----------------------------------")
            return HttpResponse("post_ok")
    try:
        if request.method == "GET":
            print(request.GET)
            host = request.GET['host']
            filename = request.GET['file']
            dirname = request.GET['dir']
            service_type = request.GET['service_type']
            urlfile = "http://%s:%s/static/upload/%s" % (serverip, serverport, filename)
            print(urlfile, dirname, service_type)
            # downloadImageFile(urlfile, dirname)
            if exec_rOOL(service_type, filename, dirname):
                # relea_time__gte=time.strftime("%Y-%m-%d")
                his_rool.objects.filter(status=1, host=host, filename=filename,
                                        relea_time__gte=time.strftime("%Y-%m-%d"),
                                        relea_time=request.GET['time']).update(status=2)
                print("----------------------update status ok----------------------------------")
                return HttpResponse("GET_ok")
    except Exception, e:
        print e
    return HttpResponse("ok")


def downloadImageFile(imgUrl, dirname):
    if dirname[-1] != '/':
        dirname += '/'
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    local_filename = imgUrl.split('/')[-1]
    print("Download Image File=", local_filename)
    r = requests.get(imgUrl, stream=True)  # here we need to set stream = True parameter
    with open(dirname + local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    return local_filename


def exec_rele(service_type, filename, dirname):
    jy_dirname = time.strftime("%Y%m%d%H%M")  # 解压后的create目录名
    jt_dir = filename.split('.')[0]
    if dirname[-1] != '/':
        dirname += '/'
    # shutil.unpack_archive('%s%s' % (dirname, filename), extract_dir=jy_dirname)
    t = tarfile.open("%s%s" % (dirname, filename))
    t.extractall(path="%s%s" % (dirname, jy_dirname))
    abs_path = os.path.abspath("%s%s/%s" % (dirname, jy_dirname, jt_dir))
#AttributeError: 'unicode' object has no attribute 'objects'
    demo_path = servicetype.objects.all()
    for i in demo_path:
        service_processname=i.service_processname
        demo_path = i.demo_path
        os.system("service %s stop"%service_processname)
        os.system("rm -rf %s/%sbak" % (demo_path, jt_dir,))
        os.system("cp -r %s/%s %s/%sbak" % (demo_path, jt_dir, demo_path, jt_dir))
        os.system("rm -rf %s/%s" % (demo_path, jt_dir))
        os.system("ln -s %s %s/%s" % (abs_path, demo_path, jt_dir))
        os.system("service %s start"%service_processname)
        jc = os.popen("ps -ef |grep -v grep|grep %s"%service_processname).read().strip()
        if os.path.isdir("%s/%s" % (demo_path, jt_dir)) and jc:
            return True

    # if service_type == "apache":
    #     os.system("service httpd stop")
    #     os.system("rm -rf %s/%sbak" % (apache_path, jt_dir,))
    #     os.system("cp -r %s/%s %s/%sbak" % (apache_path, jt_dir, apache_path, jt_dir))
    #     os.system("rm -rf %s/%s" % (apache_path, jt_dir))
    #     os.system("ln -s %s %s/%s" % (abs_path, apache_path, jt_dir))
    #     os.system("service httpd start")
    #     jc = os.popen("ps -ef |grep -v grep|grep httpd").read().strip()
    #     if os.path.isdir("%s/%s" % (apache_path, jt_dir)) and jc:
    #         return True
    #
    # if service_type == "nginx":
    #     os.system("service nginx stop")
    #     os.system("rm -rf %s/%sbak" % (nginx_path, jt_dir,))
    #     os.system("cp -r %s/%s %s/%sbak" % (nginx_path, jt_dir, nginx_path, jt_dir))
    #     os.system("rm -rf %s/%s" % (nginx_path, jt_dir))
    #     os.system("ln -s %s %s/%s" % (abs_path, nginx_path, jt_dir,))
    #     os.system("service nginx start")
    #     jc = os.popen("ps -ef |grep -v grep|grep nginx").read().strip()
    #     if os.path.isdir("/%s/%s" % (nginx_path, jt_dir)) and jc:
    #         return True
    #
    # pass


def exec_rOOL(service_type, filename, dirname):
    jy_dirname = time.strftime("%Y%m%d%H%M")  # 解压后的create目录名
    jt_dir = filename.split('.')[0]
    if dirname[-1] != '/':
        dirname += '/'
    # shutil.unpack_archive('%s%s' % (dirname, filename), extract_dir=jy_dirname)
    # t = tarfile.open("%s%s"%(dirname,filename))
    # t.extractall(path="%s%s"%(dirname,jy_dirname))
    abs_path = os.path.abspath("%s%s/%s" % (dirname, jy_dirname, jt_dir))
    demo_path = servicetype.objects.all()
    for i in demo_path:
        service_processname = i.service_processname
        demo_path = i.demo_path
        os.system("service %s stop"%service_processname)
        os.system("rm -rf %s/%s" % (demo_path, jt_dir,))
        os.system("cp -r %s/%sbak %s/%s" % (demo_path, jt_dir, demo_path, jt_dir))
        os.system("service %s start"%service_processname)
        jc = os.popen("ps -ef |grep -v grep|grep %s"%service_processname).read().strip()
        if os.path.isdir("%s/%s" % (demo_path, jt_dir)) and jc:
            return True

    # if service_type == "apache":
    #     os.system("service httpd stop")
    #     os.system("rm -rf %s/%s" % (apache_path, jt_dir,))
    #     os.system("cp -r %s/%sbak %s/%s" % (apache_path, jt_dir, apache_path, jt_dir))
    #     os.system("service httpd start")
    #     jc = os.popen("ps -ef |grep -v grep|grep httpd").read().strip()
    #     if os.path.isdir("%s/%s" % (apache_path, jt_dir)) and jc:
    #         return True
    #
    # if service_type == "nginx":
    #     os.system("service nginx stop")
    #     os.system("rm -rf %s/%s" % (nginx_path, jt_dir,))
    #     os.system("cp -r %s/%sbak %s/%s" % (nginx_path, jt_dir, nginx_path, jt_dir))
    #     # os.system("rm -rf %s/%s" % (nginx_path,jt_dir))
    #     # os.system("ln -s %s %s/%s" % (abs_path, nginx_path,jt_dir,))
    #     os.system("service nginx start")
    #     jc = os.popen("ps -ef |grep -v grep|grep nginx").read().strip()
    #     if os.path.isdir("/%s/%s" % (nginx_path, jt_dir)) and jc:
    #         return True
    #
    # pass
