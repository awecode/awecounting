# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20151217_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(related_name='item_unit', on_delete=django.db.models.deletion.SET_NULL, to='inventory.Unit', null=True),
        ),
    ]
