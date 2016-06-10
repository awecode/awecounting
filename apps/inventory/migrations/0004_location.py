# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-10 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20160530_2004'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=150)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
    ]
