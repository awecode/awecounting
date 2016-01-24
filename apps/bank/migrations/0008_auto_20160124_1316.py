# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0007_file_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='electronicfundtransferin',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='electronicfundtransferin',
            name='bank_account',
        ),
        migrations.RemoveField(
            model_name='electronicfundtransferin',
            name='benefactor',
        ),
        migrations.RemoveField(
            model_name='electronicfundtransferin',
            name='company',
        ),
        migrations.RemoveField(
            model_name='electronicfundtransferinrow',
            name='electronic_fund_transfer_in',
        ),
        migrations.RemoveField(
            model_name='electronicfundtransferout',
            name='bank_account',
        ),
        migrations.RemoveField(
            model_name='electronicfundtransferout',
            name='beneficiary',
        ),
        migrations.RemoveField(
            model_name='electronicfundtransferout',
            name='company',
        ),
        migrations.RemoveField(
            model_name='file',
            name='cheque_deposit',
        ),
        migrations.RemoveField(
            model_name='bankcashdeposit',
            name='status',
        ),
        migrations.RemoveField(
            model_name='chequedeposit',
            name='status',
        ),
        migrations.RemoveField(
            model_name='chequepayment',
            name='status',
        ),
        migrations.DeleteModel(
            name='ElectronicFundTransferIn',
        ),
        migrations.DeleteModel(
            name='ElectronicFundTransferInRow',
        ),
        migrations.DeleteModel(
            name='ElectronicFundTransferOut',
        ),
        migrations.DeleteModel(
            name='File',
        ),
    ]
