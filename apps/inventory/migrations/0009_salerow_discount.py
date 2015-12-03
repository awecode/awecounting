# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_purchaserow_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='salerow',
            name='discount',
            field=models.FloatField(default=0),
        ),
    ]
