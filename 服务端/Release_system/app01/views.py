from django.shortcuts import render
from django.shortcuts import render, HttpResponse, HttpResponsePermanentRedirect, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.shortcuts import render, render_to_response
from django import forms
from app01 import models
# from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import json, requests, threading, copy, os, sys, shutil, time, json, pymysql, collections, requests
from multiprocessing import Process
# mysql连接#
from Release_system import settings

host = settings.DATABASES['default']['HOST']  
port = settings.DATABASES['default']['PORT']  
user = settings.DATABASES['default']['USER']  
passwd = settings.DATABASES['default']['PASSWORD']  
db = settings.DATABASES['default']['NAME']  # 'daxiangzhanshi'


def acc_login(request):
    if request.method == "POST":
        print(request.POST)
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        try:
            if user:
                login(request, user)
                return redirect('/')
            else:
                error = "用户名或密码不对"
                return render(request, "login.html", {"login_error": error})
        except Exception:
            return render(request, "login.html", {"login_error": "用户名或密码不对"})
    return render(request, "login.html")


@login_required
def index(request):
    return render(request, "newindex.html")


@login_required
def acc_logout(requrst):
    logout(requrst)
    return redirect("/")


from django import forms
from app01.models import User


class UserForm(forms.Form):
    用户 = forms.CharField()
    文件 = forms.FileField()


@login_required
def register(request):
    data = models.User.objects.all()
    data1 = models.service_type.objects.all()

    if request.GET:
        print(request.GET)
        username = request.GET['user']
        address = request.GET['address']
        service_type = request.GET['service']
        updatetime = time.strftime('%Y-%m-%d %H:%M:%S')
        git_svn = request.GET['sex']
        if address:
            if git_svn == "git":
                print("-------------------------git------------------------")
                os.system("cd static/upload && git clone %s" % address)
                dirname = address.split("/")[-1].split(".")[0]
                print(dirname)
                shutil.make_archive("static/upload/%s" % dirname, 'gztar', root_dir='static/upload/%s' % dirname)
                user = User()
                user.username = username
                user.headImg = '%s.tar.gz' % dirname
                user.service_type = service_type
                user.updatetime = updatetime
                user.save()
                return render(request, "register.html", {"get": "成功拉取代码文件到服务端", "data": data, "data1": data1})

            elif git_svn == 'svn':
                print("-------------------------svn------------------------")
                svnuser = request.GET['svnuser']
                svnpass = request.GET['svnpass']
                os.system(
                    "cd static/upload && svn checkout %s --username=%s --password=%s" % (address, svnuser, svnpass))
                dirname = address.split("/")[-1]
                print(dirname)
                shutil.make_archive("static/upload/%s" % dirname, 'gztar', root_dir='static/upload/%s' % dirname)
                user = User()
                user.username = username
                user.headImg = '%s.tar.gz' % dirname
                user.service_type = service_type
                user.updatetime = updatetime
                user.save()
                return render(request, "register.html", {"get1": "成功拉取代码文件到服务端", "data": data, "data1": data1})

    if request.method == "POST":
        uf = UserForm(request.POST, request.FILES)
        if uf.is_valid():
            # 获取表单信息
            username = uf.cleaned_data['用户']
            headImg = uf.cleaned_data['文件']
            service_type = request.POST['service']
            updatetime = time.strftime('%Y-%m-%d %H:%M:%S')
            # print(headImg)
            # 写入数据库
            user = User()
            user.username = username
            user.headImg = headImg
            user.service_type = service_type
            user.updatetime = updatetime
            user.save()
            updatesql(headImg)
            print(headImg)
            return render(request, "register.html", {'uf': uf, "put": "上传成功", "data": data, "data1": data1})
    else:
        uf = UserForm()

    # return render_to_response('register.html', {'uf': uf},)
    return render(request, "register.html", {'uf': uf, "data": data, "data1": data1})


@login_required
def releases(request):
    data = models.User.objects.all()
    data1 = models.service_type.objects.all()
    data2 = models.host_list.objects.all()
    data3 = models.host_list.objects.all().values('host_group').annotate(count=Count('host_group')).values('host_group',
                                                                                                           'count')
    host_groups = []
    for i in data3:
        # print(i['host_group'])
        host_groups.append(i['host_group'])

    # print(host_groups)
    def cz_host(payload):
        time_strftime = time.strftime('%Y-%m-%d %H:%M:%S')
        payload['time'] = time_strftime
        b = models.his_rel(host=payload['host'], host_group=payload['host_group'], filename=payload['file'],
                           service_type=payload['service_type'],
                           status=1, relea_time=time_strftime)

        b.save()

        url = "http://{}:9999/".format(payload['host'])
        print(url)
        ### 1、首先登陆任何页面，获取cookie
        i1 = requests.get(url=url)
        ### 2、用户登陆，携带上一次的cookie，后台对cookie中的 gpsd 进行授权
        i2 = requests.post(
            url=url,
            data=payload,
            cookies=i1.cookies.get_dict()
        )

    if request.method == "POST":
        print(request.POST)
        payload = {'host': request.POST['host'], 'host_group': request.POST['host_group'],
                   'file': request.POST['file'], 'service_type': request.POST['service'],
                   'dir': request.POST['dir'], "cmd": request.POST['cmd']}
        if request.POST['host'] != "未选择请选择":
            hostip = models.host_list.objects.filter(hostname=request.POST['host'])
            for i in hostip:
                payload['host'] = i.ip
            cz_host(payload)
            return render(request, 'release.html',
                          {"data": data, "post_ok": "提交成功", "data3": host_groups, "data2": data2, "data1": data1})

        if request.POST['host_group'] != "未选择请选择":
            get_ip_list = models.host_list.objects.filter(host_group=request.POST['host_group'])
            # 多线程执行
            for i in get_ip_list:
                # print(i.ip)
                payload = copy.deepcopy(payload)
                payload["host"] = i.ip
                t = threading.Thread(target=cz_host, args=(payload,))
                t.start()
            return render(request, 'release.html',
                          {"data": data, "post_ok": "提交成功", "data3": host_groups, "data2": data2, "data1": data1})
    return render(request, 'release.html', {"data": data, "data3": host_groups, "data2": data2, "data1": data1})


def updatesql(name):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db,
                           charset='UTF8')

    cur = conn.cursor()
    sql = " update app01_user set headImg=replace(headImg,left(headImg,14),'') where headImg like '%{}'".format(name)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


@login_required
def release_status(request):
    data = models.his_rel.objects.all().order_by('-relea_time')[:50]
    if request.GET:
        print(request.GET)
        d = models.his_rel(id=request.GET['_id'])
        d.delete()
    return render(request, 'release_status.html', {"data": data})


@login_required
def rollback(request):
    data = models.User.objects.all()
    data1 = models.service_type.objects.all()
    data2 = models.host_list.objects.all()
    data3 = models.host_list.objects.all().values('host_group').annotate(count=Count('host_group')).values('host_group',
                                                                                                           'count')
    host_groups = []
    for i in data3:
        # print(i['host_group'])
        host_groups.append(i['host_group'])

    def cz_host(payload):
        time_strftime = time.strftime('%Y-%m-%d %H:%M:%S')
        payload['time'] = time_strftime
        b = models.his_rool(host=payload['host'], host_group=payload['host_group'], filename=payload['file'],
                            service_type=payload['service_type'],
                            status=1, relea_time=payload['time'])

        b.save()
        url = "http://{}:9999/".format(payload['host'])
        print(url)
        ret = requests.get(url, params=payload)

    if request.method == "POST":
        print(request.POST)
        payload = {'host': request.POST['host'], 'host_group': request.POST['host_group'],
                   'file': request.POST['file'], 'service_type': request.POST['service'],
                   'dir': request.POST['dir']}
        if request.POST['host'] != "未选择请选择":
            # payload = {'host': request.POST['host'], 'host_group': request.POST['host_group'],
            #            'file': request.POST['file'], 'service_type': request.POST['service'],
            #            'dir': request.POST['dir']}
            hostip = models.host_list.objects.filter(hostname=request.POST['host'])
            for i in hostip:
                payload['host'] = i.ip
            cz_host(payload)
            return render(request, 'release.html',
                          {"data": data, "post_ok": "提交成功", "data3": host_groups, "data2": data2, "data1": data1})

        if request.POST['host_group'] != "未选择请选择":
            get_ip_list = models.host_list.objects.filter(host_group=request.POST['host_group'])
            # 多线程执行
            for i in get_ip_list:
                # print(i.ip)
                payload = copy.deepcopy(payload)
                payload["host"] = i.ip
                t = threading.Thread(target=cz_host, args=(payload,))
                t.start()

            return render(request, 'Rollback.html',
                          {"data": data, "post_ok": "提交成功", "data3": host_groups, "data2": data2, "data1": data1})

    return render(request, 'Rollback.html', {"data": data, "data3": host_groups, "data2": data2, "data1": data1})


@login_required
def rollback_status(request):
    data = models.his_rool.objects.all().order_by('-relea_time')[:50]
    if request.GET:
        print(request.GET)
        d = models.his_rool(id=request.GET['_id'])
        d.delete()
    return render(request, 'rollback_status.html', {"data": data})
