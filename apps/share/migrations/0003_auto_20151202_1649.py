# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20151202_1546'),
        ('share', '0002_auto_20151202_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='investment',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shareholder',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
    ]
