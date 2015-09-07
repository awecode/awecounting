# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_inventoryaccount_current_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitConverter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_unit', models.CharField(max_length=250)),
                ('to', models.CharField(max_length=250)),
                ('multiple', models.FloatField()),
            ],
        ),
    ]
