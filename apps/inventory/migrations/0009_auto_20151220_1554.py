# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20151219_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
    ]
