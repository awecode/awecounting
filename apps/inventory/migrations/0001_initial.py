# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
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
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dr_amount', models.FloatField(null=True, blank=True)),
                ('cr_amount', models.FloatField(null=True, blank=True)),
                ('current_balance', models.FloatField(null=True, blank=True)),
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
            ],
        ),
        migrations.CreateModel(
            name='UnitConversion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('multiple', models.FloatField()),
                ('base_unit', models.ForeignKey(related_name='base_conversions', to='inventory.Unit', null=True)),
            ],
        ),
    ]
