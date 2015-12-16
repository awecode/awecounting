# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_data-groups_20151008_1930'),
        ('inventory', '0007_party_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sale',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
    ]
