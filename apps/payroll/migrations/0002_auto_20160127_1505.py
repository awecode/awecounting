# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancevoucher',
            name='from_date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
        migrations.AlterField(
            model_name='attendancevoucher',
            name='to_date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
    ]
