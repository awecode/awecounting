# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20151202_1546'),
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='journalentry',
            name='company',
            field=models.ForeignKey(related_name='ledger_journal_entry', default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='company',
            field=models.ForeignKey(related_name='ledger_transaction', default=1, to='users.Company'),
            preserve_default=False,
        ),
    ]
