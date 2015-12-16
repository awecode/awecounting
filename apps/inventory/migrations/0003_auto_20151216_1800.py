# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20151216_1529'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='party',
            unique_together=set([('pan_no', 'company')]),
        ),
    ]
