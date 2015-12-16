# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_unitconverter_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unitconverter',
            name='company',
        ),
    ]
