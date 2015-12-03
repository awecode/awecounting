# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_item_ledger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='short_name',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
