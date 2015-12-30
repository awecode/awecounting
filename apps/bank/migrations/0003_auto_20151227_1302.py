# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0002_auto_20151218_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankcashdeposit',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
    ]
