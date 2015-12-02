# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20151202_1546'),
        ('inventory', '0023_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryaccount',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='journalentry',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='party',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchase',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaserow',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sale',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salerow',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unit',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unitconverter',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
    ]
