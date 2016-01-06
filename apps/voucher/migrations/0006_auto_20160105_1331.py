# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0005_cashpayment_cashpaymentrow'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='pending_amount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='total_amount',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
