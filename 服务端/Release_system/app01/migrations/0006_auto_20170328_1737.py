# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-28 17:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_host_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='host_list',
            name='updatetime',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='host_list',
            name='hostname',
            field=models.CharField(max_length=30, verbose_name='主机名'),
        ),
    ]
