# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0002_auto_20160519_1941'),
        ('ledger', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chequepayment',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='chequedepositrow',
            name='cheque_deposit',
            field=models.ForeignKey(related_name='rows', to='bank.ChequeDeposit'),
        ),
        migrations.AddField(
            model_name='chequedeposit',
            name='bank_account',
            field=models.ForeignKey(related_name='cheque_deposits', to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='chequedeposit',
            name='benefactor',
            field=models.ForeignKey(to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='chequedeposit',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='chequedeposit',
            name='files',
            field=models.ManyToManyField(to='users.File', blank=True),
        ),
        migrations.AddField(
            model_name='bankcashdeposit',
            name='bank_account',
            field=models.ForeignKey(related_name='cash_deposits', to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='bankcashdeposit',
            name='benefactor',
            field=models.ForeignKey(to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='bankcashdeposit',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='account',
            field=models.OneToOneField(to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AlterUniqueTogether(
            name='chequedeposit',
            unique_together=set([('voucher_no', 'company')]),
        ),
        migrations.AlterUniqueTogether(
            name='bankcashdeposit',
            unique_together=set([('voucher_no', 'company')]),
        ),
    ]
