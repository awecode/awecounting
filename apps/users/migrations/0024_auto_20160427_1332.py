# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='company',
            field=models.OneToOneField(to='users.Company'),
        ),
    ]
