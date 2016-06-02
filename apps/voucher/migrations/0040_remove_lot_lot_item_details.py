# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0039_auto_20160530_1610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lot',
            name='lot_item_details',
        ),
    ]
