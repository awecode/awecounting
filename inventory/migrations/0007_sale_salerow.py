# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_purchaserow_sn'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField(null=True, blank=True)),
                ('date', models.DateField(default=datetime.datetime.today)),
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
                ('item', models.ForeignKey(to='inventory.Item')),
                ('sale', models.ForeignKey(related_name='rows', to='inventory.Sale')),
                ('unit', models.ForeignKey(to='inventory.Unit')),
            ],
        ),
    ]
