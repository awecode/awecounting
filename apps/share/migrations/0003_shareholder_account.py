# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0008_auto_20160106_1434'),
        ('share', '0002_auto_20151219_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='shareholder',
            name='account',
            field=models.ForeignKey(to='ledger.Account', null=True),
        ),
    ]
