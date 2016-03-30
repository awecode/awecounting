# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-29 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_auto_20160328_1706'),
        ('ledger', '0009_auto_20160225_1535'),
        ('voucher', '0016_auto_20160302_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_no', models.IntegerField(blank=True, null=True)),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ledger.Party')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrderRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.PositiveIntegerField()),
                ('budget_title_no', models.IntegerField(blank=True, null=True)),
                ('specification', models.CharField(blank=True, max_length=254, null=True)),
                ('quantity', models.FloatField()),
                ('unit', models.CharField(max_length=50)),
                ('rate', models.FloatField()),
                ('vattable', models.BooleanField(default=True)),
                ('remarks', models.CharField(blank=True, max_length=254, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Item')),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='voucher.PurchaseOrder')),
            ],
        ),
    ]
