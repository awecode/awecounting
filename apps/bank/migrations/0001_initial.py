# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_data-groups_20151008_1930'),
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bank_name', models.CharField(max_length=254)),
                ('ac_no', models.CharField(max_length=50)),
                ('branch_name', models.CharField(max_length=254, null=True, blank=True)),
                ('account', models.OneToOneField(to='ledger.Account')),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='BankCashDeposit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField()),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('deposited_by', models.CharField(max_length=254, null=True, blank=True)),
                ('attachment', models.FileField(null=True, upload_to=b'bank_cash_deposits/%Y/%m/%d', blank=True)),
                ('narration', models.TextField(null=True, blank=True)),
                ('status', models.CharField(default=b'Unapproved', max_length=10, choices=[(b'Approved', b'Approved'), (b'Unapproved', b'Unapproved')])),
                ('bank_account', models.ForeignKey(related_name='cash_deposits', to='ledger.Account')),
                ('benefactor', models.ForeignKey(to='ledger.Account')),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='ChequeDeposit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField()),
                ('date', models.DateField()),
                ('clearing_date', models.DateField(null=True, blank=True)),
                ('deposited_by', models.CharField(max_length=254, null=True, blank=True)),
                ('attachment', models.FileField(null=True, upload_to=b'cheque_deposits/%Y/%m/%d', blank=True)),
                ('narration', models.TextField(null=True, blank=True)),
                ('status', models.CharField(default=b'Unapproved', max_length=10, choices=[(b'Approved', b'Approved'), (b'Unapproved', b'Unapproved')])),
                ('bank_account', models.ForeignKey(related_name='cheque_deposits', to='ledger.Account')),
                ('benefactor', models.ForeignKey(to='ledger.Account')),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='ChequeDepositRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.IntegerField()),
                ('cheque_number', models.CharField(max_length=50, null=True, blank=True)),
                ('cheque_date', models.DateField(null=True, blank=True)),
                ('drawee_bank', models.CharField(max_length=254, null=True, blank=True)),
                ('drawee_bank_address', models.CharField(max_length=254, null=True, blank=True)),
                ('amount', models.FloatField()),
                ('cheque_deposit', models.ForeignKey(related_name='rows', to='bank.ChequeDeposit')),
            ],
        ),
        migrations.CreateModel(
            name='ChequePayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cheque_number', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('attachment', models.FileField(null=True, upload_to=b'cheque_payments/%Y/%m/%d', blank=True)),
                ('narration', models.TextField(null=True, blank=True)),
                ('status', models.CharField(default=b'Unapproved', max_length=10, choices=[(b'Approved', b'Approved'), (b'Unapproved', b'Unapproved')])),
                ('bank_account', models.ForeignKey(related_name='cheque_payments', to='ledger.Account')),
                ('beneficiary', models.ForeignKey(to='ledger.Account')),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='ElectronicFundTransferIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField()),
                ('date', models.DateField()),
                ('clearing_date', models.DateField(null=True, blank=True)),
                ('attachment', models.FileField(null=True, upload_to=b'electronic_fund_transfer_in/%Y/%m/%d', blank=True)),
                ('narration', models.TextField(null=True, blank=True)),
                ('status', models.CharField(default=b'Unapproved', max_length=10, choices=[(b'Approved', b'Approved'), (b'Unapproved', b'Unapproved')])),
                ('bank_account', models.ForeignKey(related_name='electronic_fund_transfer_in', to='ledger.Account')),
                ('benefactor', models.ForeignKey(to='ledger.Account')),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='ElectronicFundTransferInRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.IntegerField()),
                ('transaction_number', models.CharField(max_length=50, null=True, blank=True)),
                ('transaction_date', models.DateField(null=True, blank=True)),
                ('drawee_bank', models.CharField(max_length=254, null=True, blank=True)),
                ('drawee_bank_address', models.CharField(max_length=254, null=True, blank=True)),
                ('amount', models.FloatField()),
                ('electronic_fund_transfer_in', models.ForeignKey(related_name='rows', to='bank.ElectronicFundTransferIn')),
            ],
        ),
        migrations.CreateModel(
            name='ElectronicFundTransferOut',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_number', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('attachment', models.FileField(null=True, upload_to=b'electronic_fund_transfer_out/%Y/%m/%d', blank=True)),
                ('narration', models.TextField(null=True, blank=True)),
                ('status', models.CharField(default=b'Unapproved', max_length=10, choices=[(b'Approved', b'Approved'), (b'Unapproved', b'Unapproved')])),
                ('bank_account', models.ForeignKey(related_name='electronic_fund_transfer_out', to='ledger.Account')),
                ('beneficiary', models.ForeignKey(to='ledger.Account')),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='electronicfundtransferin',
            unique_together=set([('voucher_no', 'company')]),
        ),
        migrations.AlterUniqueTogether(
            name='chequedeposit',
            unique_together=set([('voucher_no', 'company')]),
        ),
        migrations.AlterUniqueTogether(
            name='bankcashdeposit',
            unique_together=set([('voucher_no', 'company')]),
        ),
    ]
