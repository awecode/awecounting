# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_auto_20150908_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='code',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
