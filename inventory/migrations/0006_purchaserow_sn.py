# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20150827_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaserow',
            name='sn',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
