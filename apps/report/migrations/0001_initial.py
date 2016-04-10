# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_pin_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('show_root_categories_only', models.BooleanField(verbose_name=False)),
                ('show_zero_balance_ledgers', models.BooleanField(verbose_name=False)),
                ('show_zero_balance_categories', models.BooleanField(verbose_name=False)),
                ('hide_all_ledgers', models.BooleanField(verbose_name=False)),
                ('show_ledgers_only', models.BooleanField(verbose_name=False)),
                ('company', models.OneToOneField(related_name='report_settings', to='users.Company')),
            ],
        ),
    ]
