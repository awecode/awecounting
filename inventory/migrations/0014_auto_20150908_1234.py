# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_unitconverter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unitconverter',
            name='item_unit',
        ),
        migrations.RemoveField(
            model_name='unitconverter',
            name='to',
        ),
        migrations.AddField(
            model_name='unitconverter',
            name='base_unit',
            field=models.ForeignKey(related_name='base_unit', to='inventory.Unit', null=True),
        ),
        migrations.AddField(
            model_name='unitconverter',
            name='unit_to_convert',
            field=models.ForeignKey(to='inventory.Unit', null=True),
        ),
    ]
