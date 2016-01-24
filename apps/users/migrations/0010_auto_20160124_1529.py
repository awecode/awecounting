# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20160124_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='file',
            name='object_id',
        ),
    ]
