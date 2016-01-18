# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_sale_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='due_date',
            field=njango.fields.BSDateField(null=True, blank=True),
        ),
    ]
