#!/usr/bin/env python
#coding:utf-8
import os
import sys

if __name__ == "__main__":
    try:
        import pymysql,requests,django
    except Exception:
        print ("安装插件")
        os.system("yum -y install epel-release")
        os.system("yum -y install python-pip")
        os.system("pip install --upgrade pip")
        os.system("pip install pymysql")
        os.system("pip install requests")
        os.system("pip install django")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "release_clint.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
