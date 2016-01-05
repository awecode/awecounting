# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0006_auto_20160105_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashpaymentrow',
            name='discount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='cashpaymentrow',
            unique_together=set([('invoice', 'cash_payment')]),
        ),
        migrations.AlterUniqueTogether(
            name='cashreceiptrow',
            unique_together=set([('invoice', 'cash_receipt')]),
        ),
    ]
