# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0002_auto_20151203_1412'),
        ('users', '0003_data-groups_20151008_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalVoucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField()),
                ('date', models.DateField()),
                ('narration', models.TextField()),
                ('status', models.CharField(default=b'Unapproved', max_length=10, choices=[(b'Cancelled', b'Cancelled'), (b'Approved', b'Approved'), (b'Unapproved', b'Unapproved')])),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='JournalVoucherRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'Dr', max_length=2, choices=[(b'Dr', b'Dr'), (b'Cr', b'Dr')])),
                ('description', models.TextField()),
                ('dr_amount', models.FloatField(null=True, blank=True)),
                ('cr_amount', models.FloatField(null=True, blank=True)),
                ('account', models.ForeignKey(related_name='account_rows', to='ledger.Account')),
                ('journal_voucher', models.ForeignKey(related_name='rows', to='account.JournalVoucher')),
            ],
        ),
    ]
