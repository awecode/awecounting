# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0040_remove_lot_lot_item_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasevoucherrow',
            name='lot_item_detail',
        ),
        migrations.AddField(
            model_name='lot',
            name='lot_item_details',
            field=models.ManyToManyField(to='voucher.LotItemDetail'),
        ),
    ]
