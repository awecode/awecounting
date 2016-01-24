# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20160124_1529'),
        ('bank', '0009_remove_chequedeposit_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='chequedeposit',
            name='file',
            field=models.ManyToManyField(to='users.File'),
        ),
    ]
