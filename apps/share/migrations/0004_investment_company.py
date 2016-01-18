# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20151229_1224'),
        ('share', '0003_shareholder_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='company',
            field=models.ForeignKey(default=None, to='users.Company'),
            preserve_default=False,
        ),
    ]
