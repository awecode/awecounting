# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-10 11:14
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0013_merge'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='category',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
