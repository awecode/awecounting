# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0004_investment_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='end_date',
            field=njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
    ]
