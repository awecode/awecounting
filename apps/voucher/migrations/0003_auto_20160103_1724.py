# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_auto_20160103_1724'),
        ('ledger', '0006_auto_20160103_1724'),
        ('users', '0007_auto_20151229_1224'),
        ('voucher', '0002_auto_20160102_1559'),
    ]

    operations = [
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
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField(null=True, blank=True)),
                ('credit', models.BooleanField(default=False)),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('due_date', njango.fields.BSDateField(null=True, blank=True)),
                ('company', models.ForeignKey(to='users.Company')),
                ('party', models.ForeignKey(to='ledger.Party')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.PositiveIntegerField()),
                ('quantity', models.FloatField()),
                ('rate', models.FloatField()),
                ('discount', models.FloatField(default=0)),
                ('item', models.ForeignKey(to='inventory.Item')),
                ('purchase', models.ForeignKey(related_name='rows', to='voucher.Purchase')),
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
                ('company', models.ForeignKey(to='users.Company')),
                ('party', models.ForeignKey(blank=True, to='ledger.Party', null=True)),
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
                ('unit', models.ForeignKey(to='inventory.Unit')),
            ],
        ),
        migrations.AlterField(
            model_name='cashreceipt',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
        migrations.AlterField(
            model_name='cashreceipt',
            name='party',
            field=models.ForeignKey(verbose_name='Receipt From', to='ledger.Party'),
        ),
        migrations.AlterField(
            model_name='cashreceiptrow',
            name='invoice',
            field=models.ForeignKey(related_name='receipts', to='voucher.Sale'),
        ),
    ]
