# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0019_auto_20160428_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='customer_account',
            field=models.OneToOneField(related_name='customer_detail', null=True, to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='party',
            name='supplier_account',
            field=models.OneToOneField(related_name='supplier_detail', null=True, to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='party',
            name='type',
            field=models.CharField(default=b'Customer', max_length=17, choices=[(b'Customer', b'Customer'), (b'Supplier', b'Supplier'), (b'Customer/Supplier', b'Customer/Supplier')]),
        ),
    ]
