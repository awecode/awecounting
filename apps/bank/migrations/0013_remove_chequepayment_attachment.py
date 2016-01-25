# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0012_auto_20160125_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chequepayment',
            name='attachment',
        ),
    ]
