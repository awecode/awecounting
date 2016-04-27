# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-27 07:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0005_auto_20160306_1353'),
        ('voucher', '0024_auto_20160427_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='salerow',
            name='tax_scheme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tax.TaxScheme'),
        ),
    ]