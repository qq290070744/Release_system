"""Release_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views as app01

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^accounts/login/$", app01.acc_login),
    url(r"^accounts/logout/$", app01.acc_logout),
    url(r"^$", app01.index),
    url(r'^file/', app01.register),
    url(r'^release/', app01.releases),
    url(r'^release_status/', app01.release_status),
    url(r'^rollback/', app01.rollback),
    url(r'^rollback_status/', app01.rollback_status),
]
