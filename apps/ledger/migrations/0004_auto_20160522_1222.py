# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0003_account_fy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='fy',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
    ]
