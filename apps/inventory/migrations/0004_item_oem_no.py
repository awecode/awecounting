# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-10 05:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20160530_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='oem_no',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]