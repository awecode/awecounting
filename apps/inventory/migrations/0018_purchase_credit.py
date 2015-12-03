# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_party_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='credit',
            field=models.BooleanField(default=False),
        ),
    ]
