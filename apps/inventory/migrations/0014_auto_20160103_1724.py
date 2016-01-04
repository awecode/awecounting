# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_auto_20160103_1724'),
        ('voucher', '0003_auto_20160103_1724'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Party',
        ),
        migrations.DeleteModel(
            name='Purchase',
        ),
        migrations.DeleteModel(
            name='PurchaseRow',
        ),
        migrations.DeleteModel(
            name='Sale',
        ),
        migrations.DeleteModel(
            name='SaleRow',
        ),
    ]
