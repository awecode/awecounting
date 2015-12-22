# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_companysetting_use_nepali_fy_system'),
    ]

    operations = [
        migrations.AddField(
            model_name='companysetting',
            name='unique_voucher_number',
            field=models.BooleanField(default=True),
        ),
    ]
