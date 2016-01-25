# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0013_remove_chequepayment_attachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankcashdeposit',
            name='attachment',
        ),
    ]
