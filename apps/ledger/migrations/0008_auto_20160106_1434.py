# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0007_merge'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('name', 'company')]),
        ),
    ]
