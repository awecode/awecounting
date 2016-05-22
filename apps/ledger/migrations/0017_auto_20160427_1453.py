# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0016_auto_20160427_1323'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='category',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='party',
            name='address',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='party',
            name='pan_no',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Tax Reg. No.', blank=True),
        ),
    ]
