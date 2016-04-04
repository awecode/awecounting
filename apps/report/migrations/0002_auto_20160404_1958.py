# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportsetting',
            name='hide_all_ledgers',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reportsetting',
            name='show_ledgers_only',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reportsetting',
            name='show_root_categories_only',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reportsetting',
            name='show_zero_balance_categories',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reportsetting',
            name='show_zero_balance_ledgers',
            field=models.BooleanField(default=False),
        ),
    ]
