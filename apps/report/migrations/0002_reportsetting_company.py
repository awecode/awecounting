# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportsetting',
            name='company',
            field=models.OneToOneField(related_name='report_settings', to='users.Company'),
        ),
    ]
