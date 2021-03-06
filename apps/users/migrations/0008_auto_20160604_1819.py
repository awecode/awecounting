# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 12:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_subscription_enable_branches'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='combine_reports',
            field=models.BooleanField(default=False, verbose_name=b'Show combined reports of branches'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='disable_head_office_vouchers',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='branch',
            name='branch_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='branch_instance', to='users.Company'),
        ),
    ]
