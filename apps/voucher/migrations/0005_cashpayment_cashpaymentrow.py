# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0006_auto_20160103_1724'),
        ('users', '0007_auto_20151229_1224'),
        ('voucher', '0004_auto_20160103_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField()),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('reference', models.CharField(max_length=50, null=True, blank=True)),
                ('amount', models.FloatField(null=True, blank=True)),
                ('description', models.TextField()),
                ('company', models.ForeignKey(to='users.Company')),
                ('party', models.ForeignKey(verbose_name='Paid To', to='ledger.Party')),
            ],
        ),
        migrations.CreateModel(
            name='CashPaymentRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment', models.FloatField()),
                ('discount', models.FloatField()),
                ('cash_payment', models.ForeignKey(related_name='rows', to='voucher.CashPayment')),
                ('invoice', models.ForeignKey(related_name='receipts', to='voucher.Purchase')),
            ],
        ),
    ]
