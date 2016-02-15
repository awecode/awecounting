# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0001_initial'),
        ('voucher', '0010_auto_20160118_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='tax',
            field=models.CharField(default='inclusive', max_length=10, null=True, blank=True, choices=[('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'), ('no', 'No Tax')]),
        ),
        migrations.AddField(
            model_name='purchase',
            name='tax_scheme',
            field=models.ForeignKey(blank=True, to='tax.TaxScheme', null=True),
        ),
    ]
