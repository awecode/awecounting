# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'items', blank=True)),
                ('size', models.CharField(max_length=250, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('address', models.CharField(max_length=254, null=True, blank=True)),
                ('phone_no', models.CharField(max_length=100, null=True, blank=True)),
                ('pan_no', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.PositiveIntegerField(null=True, blank=True)),
                ('data', models.DateField(default=datetime.datetime.today)),
                ('party', models.ForeignKey(to='inventory.Party')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField()),
                ('rate', models.FloatField()),
                ('item', models.ForeignKey(to='inventory.Item')),
                ('product', models.ForeignKey(related_name='rows', to='inventory.Purchase')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('short_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='purchaserow',
            name='unit',
            field=models.ForeignKey(to='inventory.Unit'),
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(to='inventory.Unit'),
        ),
    ]
