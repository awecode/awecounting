# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0005_auto_20160523_1421'),
    ]

    operations = [
        migrations.RenameField(
            model_name='party',
            old_name='customer_ledger',
            new_name='customer_account',
        ),
        migrations.RenameField(
            model_name='party',
            old_name='supplier_ledger',
            new_name='supplier_account',
        ),
    ]
