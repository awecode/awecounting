# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_auto_20160103_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='party',
            name='account',
        ),
        migrations.RemoveField(
            model_name='party',
            name='company',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='company',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='party',
        ),
        migrations.RemoveField(
            model_name='purchaserow',
            name='item',
        ),
        migrations.RemoveField(
            model_name='purchaserow',
            name='purchase',
        ),
        migrations.RemoveField(
            model_name='purchaserow',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='company',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='party',
        ),
        migrations.RemoveField(
            model_name='salerow',
            name='item',
        ),
        migrations.RemoveField(
            model_name='salerow',
            name='sale',
        ),
        migrations.RemoveField(
            model_name='salerow',
            name='unit',
        ),
    ]
