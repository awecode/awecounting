# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20160427_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enable_purchase', models.BooleanField(default=True)),
                ('enable_purchase_order', models.BooleanField(default=True)),
                ('enable_sales', models.BooleanField(default=True)),
                ('enable_cash_vouchers', models.BooleanField(default=True)),
                ('enable_journal_voucher', models.BooleanField(default=True)),
                ('enable_fixed_assets_voucher', models.BooleanField(default=True)),
                ('enable_bank_vouchers', models.BooleanField(default=True)),
                ('enable_share_management', models.BooleanField(default=True)),
                ('enable_payroll', models.BooleanField(default=True)),
                ('enable_reports', models.BooleanField(default=True)),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
    ]
