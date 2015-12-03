# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_data-groups_20151008_1930'),
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='company',
            field=models.ForeignKey(default=None, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='company',
            field=models.ForeignKey(default=None, to='users.Company'),
            preserve_default=False,
        ),
    ]
