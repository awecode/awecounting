# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0011_auto_20160331_1215'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='category',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='party',
            name='related_company',
            field=models.OneToOneField(related_name='related_party', null=True, blank=True, to='users.Company'),
        ),
    ]
