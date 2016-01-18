# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_auto_20151227_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chequedeposit',
            name='clearing_date',
            field=njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chequedeposit',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
        migrations.AlterField(
            model_name='chequedepositrow',
            name='cheque_date',
            field=njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True),
        ),
    ]
