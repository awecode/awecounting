# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20160528_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='enable_branches',
            field=models.BooleanField(default=False),
        ),
    ]