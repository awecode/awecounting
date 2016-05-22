# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_auto_20160427_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='company',
            field=models.OneToOneField(related_name='subscription', to='users.Company'),
        ),
    ]
