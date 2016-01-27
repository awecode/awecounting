# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_purchase_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='pending_amount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='total_amount',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
