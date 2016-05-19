# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0001_initial'),
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chequepayment',
            name='bank_account',
            field=models.ForeignKey(related_name='cheque_payments', to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='chequepayment',
            name='beneficiary',
            field=models.ForeignKey(to='ledger.Account'),
        ),
    ]
