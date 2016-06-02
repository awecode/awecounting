# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0037_auto_20160530_1328'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchasevoucherrow',
            old_name='lot_item_details',
            new_name='lot_item_detail',
        ),
    ]
