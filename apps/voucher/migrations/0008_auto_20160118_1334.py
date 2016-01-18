# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0008_auto_20160106_1434'),
        ('users', '0007_auto_20151229_1224'),
        ('voucher', '0007_auto_20160105_1624'),
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
            name='FixedAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField()),
                ('date', models.DateField()),
                ('reference', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.TextField()),
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
        migrations.AddField(
            model_name='additionaldetail',
            name='fixed_asset',
            field=models.ForeignKey(related_name='additional_details', to='voucher.FixedAsset'),
        ),
    ]
