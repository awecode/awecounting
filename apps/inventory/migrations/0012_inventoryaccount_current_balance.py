# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_journalentry_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryaccount',
            name='current_balance',
            field=models.FloatField(default=0),
        ),
    ]
