# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0009_auto_20160118_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixedasset',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
