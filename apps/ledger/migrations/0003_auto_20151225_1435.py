# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0002_journalvoucher_journalvoucherrow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalvoucherrow',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
