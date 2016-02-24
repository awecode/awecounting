# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0001_initial'),
        ('voucher', '0011_auto_20160215_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaserow',
            name='tax_scheme',
            field=models.ForeignKey(blank=True, to='tax.TaxScheme', null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='tax',
            field=models.CharField(default='inclusive', max_length=10, null=True, blank=True, choices=[('no', 'No Tax'), ('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive')]),
        ),
    ]
