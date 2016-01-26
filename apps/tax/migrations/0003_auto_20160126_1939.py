# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0002_auto_20160126_1932'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taxscheme',
            old_name='name',
            new_name='full_name',
        ),
    ]
