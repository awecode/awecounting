# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0020_auto_20160428_1605'),
    ]

    operations = [
        migrations.RenameField(
            model_name='party',
            old_name='customer_account',
            new_name='customer_ledger',
        ),
        migrations.RenameField(
            model_name='party',
            old_name='supplier_account',
            new_name='supplier_ledger',
        ),
    ]
