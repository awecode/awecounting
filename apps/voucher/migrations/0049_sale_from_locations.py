# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-10 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20160610_1516'),
        ('voucher', '0048_purchasevoucherrow_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='from_locations',
            field=models.ManyToManyField(blank=True, to='inventory.Location'),
        ),
    ]
