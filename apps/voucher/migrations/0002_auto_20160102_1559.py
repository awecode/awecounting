# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-02 10:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cashreceipt',
            old_name='receipt_on',
            new_name='date',
        ),
    ]
