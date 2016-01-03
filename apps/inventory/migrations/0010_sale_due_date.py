# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20151220_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='due_date',
            field=njango.fields.BSDateField(null=True, blank=True),
        ),
    ]
