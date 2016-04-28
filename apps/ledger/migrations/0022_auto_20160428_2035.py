# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0021_auto_20160428_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='type',
            field=models.CharField(default=b'Customer/Supplier', max_length=17, choices=[(b'Customer', b'Customer'), (b'Supplier', b'Supplier'), (b'Customer/Supplier', b'Customer/Supplier')]),
        ),
    ]
