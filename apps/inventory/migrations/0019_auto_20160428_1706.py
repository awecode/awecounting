# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0021_auto_20160428_1706'),
        ('inventory', '0018_auto_20160328_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='purchase_ledger',
            field=models.OneToOneField(related_name='purchase_detail', null=True, to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='item',
            name='sale_ledger',
            field=models.OneToOneField(related_name='sale_detail', null=True, to='ledger.Account'),
        ),
    ]
