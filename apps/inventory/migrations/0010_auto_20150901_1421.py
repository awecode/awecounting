# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_salerow_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('account_no', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='account',
            field=models.OneToOneField(related_name='item', null=True, to='apps.inventory.InventoryAccount'),
        ),
    ]
