# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_companysetting'),
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalVoucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_no', models.IntegerField()),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('narration', models.TextField()),
                ('status', models.CharField(default=b'Unapproved', max_length=10, choices=[(b'Cancelled', b'Cancelled'), (b'Approved', b'Approved'), (b'Unapproved', b'Unapproved')])),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='JournalVoucherRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'Dr', max_length=2, choices=[(b'Dr', b'Dr'), (b'Cr', b'Cr')])),
                ('description', models.TextField()),
                ('dr_amount', models.FloatField(null=True, blank=True)),
                ('cr_amount', models.FloatField(null=True, blank=True)),
                ('account', models.ForeignKey(related_name='account_rows', to='ledger.Account')),
                ('journal_voucher', models.ForeignKey(related_name='rows', to='ledger.JournalVoucher')),
            ],
        ),
    ]
