# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='start_date',
            field=njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True),
        ),
    ]
