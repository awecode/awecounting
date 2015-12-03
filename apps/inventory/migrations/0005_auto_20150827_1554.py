# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20150827_1458'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='data',
            new_name='date',
        ),
    ]
