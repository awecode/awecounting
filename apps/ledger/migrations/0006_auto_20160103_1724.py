# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20151229_1224'),
        ('ledger', '0005_auto_20160103_1258'),
    ]

    operations = [
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
                ('account', models.ForeignKey(to='ledger.Account', null=True)),
                ('company', models.ForeignKey(to='users.Company')),
            ],
            options={
                'verbose_name_plural': 'Parties',
            },
        ),
        migrations.RemoveField(
            model_name='journalvoucher',
            name='company',
        ),
        migrations.RemoveField(
            model_name='journalvoucherrow',
            name='account',
        ),
        migrations.RemoveField(
            model_name='journalvoucherrow',
            name='journal_voucher',
        ),
        migrations.DeleteModel(
            name='JournalVoucher',
        ),
        migrations.DeleteModel(
            name='JournalVoucherRow',
        ),
    ]
