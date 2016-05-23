# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0004_auto_20160522_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='code',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='code',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('company', 'name')]),
        ),
    ]
