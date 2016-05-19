# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10, null=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('current_dr', models.FloatField(null=True, blank=True)),
                ('current_cr', models.FloatField(null=True, blank=True)),
                ('tax_rate', models.FloatField(null=True, blank=True)),
                ('opening_dr', models.FloatField(default=0)),
                ('opening_cr', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=254, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('object_id', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name_plural': 'Journal Entries',
            },
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('name_en', models.CharField(max_length=254, null=True)),
                ('name_ne', models.CharField(max_length=254, null=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('phone_no', models.CharField(max_length=100, null=True, blank=True)),
                ('pan_no', models.CharField(max_length=50, null=True, verbose_name=b'Tax Reg. No.', blank=True)),
                ('type', models.CharField(default=b'Customer/Supplier', max_length=17, choices=[(b'Customer', b'Customer'), (b'Supplier', b'Supplier'), (b'Customer/Supplier', b'Customer/Supplier')])),
                ('account', models.ForeignKey(to='ledger.Account', null=True)),
            ],
            options={
                'verbose_name_plural': 'Parties',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dr_amount', models.FloatField(null=True, blank=True)),
                ('cr_amount', models.FloatField(null=True, blank=True)),
                ('current_dr', models.FloatField(null=True, blank=True)),
                ('current_cr', models.FloatField(null=True, blank=True)),
                ('account', models.ForeignKey(to='ledger.Account')),
                ('journal_entry', models.ForeignKey(related_name='transactions', to='ledger.JournalEntry')),
            ],
        ),
    ]
