# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-09-28 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='learn_time',
            field=models.IntegerField(default=0, verbose_name='学习时长(分钟数)'),
        ),
    ]
