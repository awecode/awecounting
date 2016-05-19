# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_auto_20160519_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='enable_bs',
            field=models.BooleanField(default=True, verbose_name=b'Enable BS Calendar'),
        ),
    ]
