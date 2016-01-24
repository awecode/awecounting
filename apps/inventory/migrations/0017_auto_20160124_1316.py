# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_auto_20160118_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitconversion',
            name='base_unit',
            field=models.ForeignKey(related_name='base_conversions', to='inventory.Unit', null=True),
        ),
        migrations.AlterField(
            model_name='unitconversion',
            name='unit_to_convert',
            field=models.ForeignKey(related_name='conversions', to='inventory.Unit', null=True),
        ),
    ]
