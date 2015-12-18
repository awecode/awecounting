# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20151217_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='credit',
            field=models.BooleanField(default=False),
        ),
    ]
