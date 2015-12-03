# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0001_initial'),
        ('inventory', '0016_item_selling_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='account',
            field=models.ForeignKey(null=True, to='apps.ledger.Account'),
            preserve_default=False,
        ),
    ]
