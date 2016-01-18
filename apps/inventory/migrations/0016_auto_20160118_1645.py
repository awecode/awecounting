# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20151229_1224'),
        ('inventory', '0015_unitconverter_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitConversion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('multiple', models.FloatField()),
                ('base_unit', models.ForeignKey(related_name='base_unit', to='inventory.Unit', null=True)),
                ('company', models.ForeignKey(to='users.Company')),
                ('unit_to_convert', models.ForeignKey(to='inventory.Unit', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='unitconverter',
            name='base_unit',
        ),
        migrations.RemoveField(
            model_name='unitconverter',
            name='company',
        ),
        migrations.RemoveField(
            model_name='unitconverter',
            name='unit_to_convert',
        ),
        migrations.DeleteModel(
            name='UnitConverter',
        ),
    ]
