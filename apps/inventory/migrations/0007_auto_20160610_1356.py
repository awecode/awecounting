# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-10 08:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20160610_1324'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='parent_location',
            new_name='parent',
        ),
    ]
