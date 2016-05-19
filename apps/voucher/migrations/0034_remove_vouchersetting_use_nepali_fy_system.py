# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0033_auto_20160515_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vouchersetting',
            name='use_nepali_fy_system',
        ),
    ]
