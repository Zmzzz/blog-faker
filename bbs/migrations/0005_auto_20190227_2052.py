# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-02-27 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0004_auto_20190227_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(default='media/avatars/default.jpg', upload_to='avatars/', verbose_name='头像'),
        ),
    ]
