# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxscheme',
            name='recoverable',
            field=models.BooleanField(default=False),
        ),
    ]
