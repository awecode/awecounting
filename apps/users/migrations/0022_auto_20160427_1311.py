# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20160406_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='type_of_business',
        ),
        migrations.AddField(
            model_name='company',
            name='organization_type',
            field=models.CharField(default=b'sole_proprietorship', max_length=254, choices=[(b'sole_proprietorship', b'Sole Proprietorship'), (b'partnership', b'Partnership'), (b'corporation', b'Corporation'), (b'non_profit', b'Non-profit')]),
        ),
        migrations.AddField(
            model_name='company',
            name='purchases_goods',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='company',
            name='purchases_services',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='company',
            name='sells_goods',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='company',
            name='sells_services',
            field=models.BooleanField(default=False),
        ),
    ]
