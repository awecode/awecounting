# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('show_root_categories_only', models.BooleanField(default=False)),
                ('show_zero_balance_ledgers', models.BooleanField(default=False)),
                ('show_zero_balance_categories', models.BooleanField(default=False)),
                ('show_ledgers_only', models.BooleanField(default=False)),
            ],
        ),
    ]
