# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_data-groups_20151008_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('account_no', models.PositiveIntegerField()),
                ('current_balance', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=250, null=True, blank=True)),
                ('name', models.CharField(max_length=254)),
                ('name_en', models.CharField(max_length=254, null=True)),
                ('name_ne', models.CharField(max_length=254, null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('description_en', models.TextField(null=True, blank=True)),
                ('description_ne', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'items', blank=True)),
                ('size', models.CharField(max_length=250, null=True, blank=True)),
                ('selling_rate', models.FloatField(null=True, blank=True)),
                ('other_properties', jsonfield.fields.JSONField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('model_id', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name_plural': 'InventoryJournal Entries',
            },
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('name_en', models.CharField(max_length=254, null=True)),
                ('name_ne', models.CharField(max_length=254, null=True)),
                ('address', models.CharField(max_length=254, null=True, blank=True)),
                ('phone_no', models.CharField(max_length=100, null=True, blank=True)),
                ('pan_no', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Parties',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField(null=True, blank=True)),
                ('credit', models.BooleanField(default=False)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('company', models.ForeignKey(to='users.Company')),
                ('party', models.ForeignKey(to='inventory.Party')),
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
                ('purchase', models.ForeignKey(related_name='rows', to='inventory.Purchase')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField(null=True, blank=True)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('company', models.ForeignKey(to='users.Company')),
                ('party', models.ForeignKey(blank=True, to='inventory.Party', null=True)),
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
                ('sale', models.ForeignKey(related_name='rows', to='inventory.Sale')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dr_amount', models.FloatField(null=True, blank=True)),
                ('cr_amount', models.FloatField(null=True, blank=True)),
                ('current_balance', models.FloatField(null=True, blank=True)),
                ('account', models.ForeignKey(to='inventory.InventoryAccount')),
                ('journal_entry', models.ForeignKey(related_name='transactions', to='inventory.JournalEntry')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('name_en', models.CharField(max_length=50, null=True)),
                ('name_ne', models.CharField(max_length=50, null=True)),
                ('short_name', models.CharField(max_length=10, null=True, blank=True)),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='UnitConverter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('multiple', models.FloatField()),
                ('base_unit', models.ForeignKey(related_name='base_unit', to='inventory.Unit', null=True)),
                ('unit_to_convert', models.ForeignKey(to='inventory.Unit', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='salerow',
            name='unit',
            field=models.ForeignKey(to='inventory.Unit'),
        ),
        migrations.AddField(
            model_name='purchaserow',
            name='unit',
            field=models.ForeignKey(to='inventory.Unit'),
        ),
    ]
