# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ledger', '0001_initial'),
        ('tax', '0001_initial'),
        ('inventory', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assets_code', models.CharField(max_length=100, null=True, blank=True)),
                ('assets_type', models.CharField(max_length=100, null=True, blank=True)),
                ('vendor_name', models.CharField(max_length=100, null=True, blank=True)),
                ('vendor_address', models.CharField(max_length=254, null=True, blank=True)),
                ('amount', models.FloatField(null=True, blank=True)),
                ('useful_life', models.CharField(max_length=254, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('warranty_period', models.CharField(max_length=100, null=True, blank=True)),
                ('maintenance', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
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
                ('discount', models.FloatField(null=True, blank=True)),
                ('cash_payment', models.ForeignKey(related_name='rows', to='voucher.CashPayment')),
            ],
        ),
        migrations.CreateModel(
            name='CashReceipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField()),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('reference', models.CharField(max_length=50, null=True, blank=True)),
                ('amount', models.FloatField(null=True, blank=True)),
                ('description', models.TextField()),
                ('company', models.ForeignKey(to='users.Company')),
                ('party', models.ForeignKey(verbose_name='Receipt From', to='ledger.Party')),
            ],
        ),
        migrations.CreateModel(
            name='CashReceiptRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receipt', models.FloatField()),
                ('discount', models.FloatField(null=True, blank=True)),
                ('cash_receipt', models.ForeignKey(related_name='rows', to='voucher.CashReceipt')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField(null=True, blank=True)),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('expense', models.ForeignKey(related_name='expense', to='ledger.Account')),
                ('expense_row', models.ForeignKey(related_name='rows', to='voucher.Expense')),
                ('pay_head', models.ForeignKey(related_name='cash_and_bank', to='ledger.Account')),
            ],
        ),
        migrations.CreateModel(
            name='FixedAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField()),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('reference', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('company', models.ForeignKey(to='users.Company')),
                ('from_account', models.ForeignKey(to='ledger.Account')),
            ],
        ),
        migrations.CreateModel(
            name='FixedAssetRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('amount', models.FloatField()),
                ('asset_ledger', models.ForeignKey(to='ledger.Account')),
                ('fixed_asset', models.ForeignKey(related_name='rows', to='voucher.FixedAsset')),
            ],
        ),
        migrations.CreateModel(
            name='JournalVoucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField()),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('narration', models.TextField()),
                ('status', models.CharField(default='Unapproved', max_length=10, choices=[('Cancelled', 'Cancelled'), ('Approved', 'Approved'), ('Unapproved', 'Unapproved')])),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='JournalVoucherRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default='Dr', max_length=2, choices=[('Dr', 'Dr'), ('Cr', 'Cr')])),
                ('description', models.TextField(null=True, blank=True)),
                ('dr_amount', models.FloatField(null=True, blank=True)),
                ('cr_amount', models.FloatField(null=True, blank=True)),
                ('account', models.ForeignKey(related_name='account_rows', to='ledger.Account')),
                ('journal_voucher', models.ForeignKey(related_name='rows', to='voucher.JournalVoucher')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField(null=True, blank=True)),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('company', models.ForeignKey(to='users.Company')),
                ('party', models.ForeignKey(to='ledger.Party')),
                ('purchase_agent', models.ForeignKey(related_name='purchase_order', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrderRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('specification', models.CharField(max_length=254, null=True, blank=True)),
                ('quantity', models.FloatField()),
                ('rate', models.FloatField()),
                ('remarks', models.CharField(max_length=254, null=True, blank=True)),
                ('item', models.ForeignKey(to='inventory.Item')),
                ('purchase_order', models.ForeignKey(related_name='rows', to='voucher.PurchaseOrder')),
                ('unit', models.ForeignKey(to='inventory.Unit')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseVoucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField(null=True, blank=True)),
                ('credit', models.BooleanField(default=False)),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('tax', models.CharField(default='inclusive', max_length=10, null=True, blank=True, choices=[('no', 'No Tax'), ('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive')])),
                ('due_date', njango.fields.BSDateField(null=True, blank=True)),
                ('pending_amount', models.FloatField(null=True, blank=True)),
                ('total_amount', models.FloatField(null=True, blank=True)),
                ('discount', models.CharField(max_length=50, null=True, blank=True)),
                ('company', models.ForeignKey(to='users.Company')),
                ('party', models.ForeignKey(to='ledger.Party')),
                ('tax_scheme', models.ForeignKey(blank=True, to='tax.TaxScheme', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseVoucherRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('quantity', models.FloatField()),
                ('rate', models.FloatField()),
                ('discount', models.CharField(max_length=50, null=True, blank=True)),
                ('item', models.ForeignKey(to='inventory.Item')),
                ('purchase', models.ForeignKey(related_name='rows', to='voucher.PurchaseVoucher')),
                ('tax_scheme', models.ForeignKey(blank=True, to='tax.TaxScheme', null=True)),
                ('unit', models.ForeignKey(to='inventory.Unit')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('credit', models.BooleanField(default=False)),
                ('voucher_no', models.PositiveIntegerField(null=True, blank=True)),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('due_date', njango.fields.BSDateField(null=True, blank=True)),
                ('pending_amount', models.FloatField(null=True, blank=True)),
                ('total_amount', models.FloatField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('tax', models.CharField(default='inclusive', max_length=10, null=True, blank=True, choices=[('no', 'No Tax'), ('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive')])),
                ('discount', models.CharField(max_length=50, null=True, blank=True)),
                ('company', models.ForeignKey(to='users.Company')),
                ('party', models.ForeignKey(blank=True, to='ledger.Party', null=True)),
                ('tax_scheme', models.ForeignKey(blank=True, to='tax.TaxScheme', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SaleRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('quantity', models.FloatField()),
                ('rate', models.FloatField()),
                ('discount', models.FloatField(default=0)),
                ('item', models.ForeignKey(to='inventory.Item')),
                ('sale', models.ForeignKey(related_name='rows', to='voucher.Sale')),
                ('tax_scheme', models.ForeignKey(blank=True, to='tax.TaxScheme', null=True)),
                ('unit', models.ForeignKey(to='inventory.Unit')),
            ],
        ),
        migrations.CreateModel(
            name='VoucherSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unique_voucher_number', models.BooleanField(default=True)),
                ('single_discount_on_whole_invoice', models.BooleanField(default=True)),
                ('discount_on_each_invoice_particular', models.BooleanField(default=False)),
                ('invoice_default_tax_application_type', models.CharField(default='exclusive', max_length=10, null=True, blank=True, choices=[('no', 'No Tax'), ('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive')])),
                ('single_discount_on_whole_purchase', models.BooleanField(default=True)),
                ('discount_on_each_purchase_particular', models.BooleanField(default=False)),
                ('purchase_default_tax_application_type', models.CharField(default='exclusive', max_length=10, null=True, blank=True, choices=[('no', 'No Tax'), ('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive')])),
                ('voucher_number_start_date', njango.fields.BSDateField(default=njango.fields.today)),
                ('company', models.OneToOneField(related_name='settings', to='users.Company')),
                ('invoice_default_tax_scheme', models.ForeignKey(related_name='default_invoice_tax_scheme', blank=True, to='tax.TaxScheme', null=True)),
                ('purchase_default_tax_scheme', models.ForeignKey(related_name='default_purchase_tax_scheme', blank=True, to='tax.TaxScheme', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='cashreceiptrow',
            name='invoice',
            field=models.ForeignKey(related_name='receipts', to='voucher.Sale'),
        ),
        migrations.AddField(
            model_name='cashpaymentrow',
            name='invoice',
            field=models.ForeignKey(related_name='receipts', to='voucher.PurchaseVoucher'),
        ),
        migrations.AddField(
            model_name='additionaldetail',
            name='fixed_asset',
            field=models.ForeignKey(related_name='additional_details', to='voucher.FixedAsset'),
        ),
        migrations.AlterUniqueTogether(
            name='cashreceiptrow',
            unique_together=set([('invoice', 'cash_receipt')]),
        ),
        migrations.AlterUniqueTogether(
            name='cashpaymentrow',
            unique_together=set([('invoice', 'cash_payment')]),
        ),
    ]
