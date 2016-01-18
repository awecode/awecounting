# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0008_auto_20160118_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixedasset',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
    ]
