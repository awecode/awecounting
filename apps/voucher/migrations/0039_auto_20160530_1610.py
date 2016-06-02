# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0038_auto_20160530_1532'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PoReceiveLot',
            new_name='Lot',
        ),
        migrations.RenameField(
            model_name='purchasevoucherrow',
            old_name='po_receive_lot',
            new_name='lot',
        ),
    ]
