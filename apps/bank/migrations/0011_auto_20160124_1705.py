# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20160124_1529'),
        ('bank', '0010_chequedeposit_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chequedeposit',
            name='file',
        ),
        migrations.AddField(
            model_name='chequedeposit',
            name='files',
            field=models.ManyToManyField(to='users.File', blank=True),
        ),
    ]
