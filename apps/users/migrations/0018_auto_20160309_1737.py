# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-09 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20160306_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pin',
            name='code',
            field=models.CharField(max_length=100),
        ),
    ]