# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bank_name', models.CharField(max_length=254)),
                ('ac_no', models.CharField(max_length=50, verbose_name='Account No.')),
                ('branch_name', models.CharField(max_length=254, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BankCashDeposit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField()),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('amount', models.FloatField()),
                ('deposited_by', models.CharField(max_length=254, null=True, blank=True)),
                ('narration', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChequeDeposit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField()),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('clearing_date', njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True)),
                ('deposited_by', models.CharField(max_length=254, null=True, blank=True)),
                ('narration', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChequeDepositRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.IntegerField()),
                ('cheque_number', models.CharField(max_length=50, null=True, blank=True)),
                ('cheque_date', njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True)),
                ('drawee_bank', models.CharField(max_length=254, null=True, blank=True)),
                ('drawee_bank_address', models.CharField(max_length=254, null=True, blank=True)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ChequePayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cheque_number', models.CharField(max_length=50)),
                ('date', njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True)),
                ('amount', models.FloatField()),
                ('narration', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
