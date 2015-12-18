# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20151216_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(related_name='item_unit', to='inventory.Unit'),
        ),
    ]
