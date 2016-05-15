# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-12 09:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_branch'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'verbose_name_plural': 'Branches'},
        ),
        migrations.AddField(
            model_name='branch',
            name='name',
            field=models.CharField(default=' ', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='branch',
            name='party',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ledger.Party'),
        ),
    ]