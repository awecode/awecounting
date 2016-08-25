# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_subscription_enable_lot'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='contact_no',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
    ]
