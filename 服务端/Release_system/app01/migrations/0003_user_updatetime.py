# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20170323_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='updatetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
