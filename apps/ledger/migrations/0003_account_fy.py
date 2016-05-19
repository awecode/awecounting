# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0002_auto_20160519_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='fy',
            field=models.PositiveSmallIntegerField(default=2072),
            preserve_default=False,
        ),
    ]
