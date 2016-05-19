# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_auto_20160515_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='enable_bs',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='company',
            name='enable_multi_language',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='company',
            name='fy_start_day',
            field=models.PositiveIntegerField(default=12),
        ),
        migrations.AddField(
            model_name='company',
            name='fy_start_month',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='company',
            name='use_nepali_fy_system',
            field=models.BooleanField(default=True),
        ),
    ]
