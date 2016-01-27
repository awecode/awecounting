# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0002_auto_20160127_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancevoucher',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
    ]
