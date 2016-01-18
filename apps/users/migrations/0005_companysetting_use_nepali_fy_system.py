# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_companysetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='companysetting',
            name='use_nepali_fy_system',
            field=models.BooleanField(default=True),
        ),
    ]
