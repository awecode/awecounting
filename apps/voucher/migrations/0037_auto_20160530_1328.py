# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20160519_1941'),
        ('voucher', '0036_poreceivelot'),
    ]

    operations = [
        migrations.CreateModel(
            name='LotItemDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qty', models.PositiveIntegerField()),
                ('item', models.ForeignKey(to='inventory.Item')),
            ],
        ),
        migrations.AddField(
            model_name='purchasevoucherrow',
            name='po_receive_lot',
            field=models.ForeignKey(blank=True, to='voucher.PoReceiveLot', null=True),
        ),
        migrations.AddField(
            model_name='poreceivelot',
            name='lot_item_details',
            field=models.ManyToManyField(to='voucher.LotItemDetail', through='voucher.PurchaseVoucherRow'),
        ),
        migrations.AddField(
            model_name='purchasevoucherrow',
            name='lot_item_details',
            field=models.ForeignKey(blank=True, to='voucher.LotItemDetail', null=True),
        ),
    ]
