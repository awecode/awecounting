# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_item_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='selling_rate',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
