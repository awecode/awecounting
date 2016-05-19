# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_data-groups_20151008_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='fy_start_day',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
