# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_sale_salerow'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaserow',
            name='discount',
            field=models.FloatField(default=0),
        ),
    ]
