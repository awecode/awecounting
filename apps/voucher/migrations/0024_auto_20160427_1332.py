# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0023_vouchersetting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vouchersetting',
            name='invoice_default_tax_application_type',
            field=models.CharField(default='exclusive', max_length=10, null=True, blank=True, choices=[('no', 'No Tax'), ('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive')]),
        ),
        migrations.AlterField(
            model_name='vouchersetting',
            name='purchase_default_tax_application_type',
            field=models.CharField(default='exclusive', max_length=10, null=True, blank=True, choices=[('no', 'No Tax'), ('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive')]),
        ),
    ]
