# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0006_remove_file_narration'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='description',
            field=models.TextField(max_length=254, null=True, blank=True),
        ),
    ]
