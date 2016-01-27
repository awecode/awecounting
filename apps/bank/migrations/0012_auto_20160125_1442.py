# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0011_auto_20160124_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chequepayment',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True),
        ),
    ]
