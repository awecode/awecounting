# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0008_auto_20160124_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chequedeposit',
            name='attachment',
        ),
    ]
