# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-02 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0014_auto_20160301_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='discount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]