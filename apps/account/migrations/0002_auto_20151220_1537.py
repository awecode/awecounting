# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalvoucher',
            name='date',
            field=njango.fields.BSDateField(default=njango.fields.today),
        ),
        migrations.AlterField(
            model_name='journalvoucherrow',
            name='type',
            field=models.CharField(default=b'Dr', max_length=2, choices=[(b'Dr', b'Dr'), (b'Cr', b'Cr')]),
        ),
    ]
