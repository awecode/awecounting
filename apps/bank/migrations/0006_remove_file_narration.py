# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0005_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='narration',
        ),
    ]
