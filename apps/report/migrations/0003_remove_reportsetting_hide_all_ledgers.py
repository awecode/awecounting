# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_auto_20160404_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportsetting',
            name='hide_all_ledgers',
        ),
    ]
