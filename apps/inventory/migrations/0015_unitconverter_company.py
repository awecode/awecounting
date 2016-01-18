# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20151229_1224'),
        ('inventory', '0014_auto_20160103_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitconverter',
            name='company',
            field=models.ForeignKey(default=1, to='users.Company'),
            preserve_default=False,
        ),
    ]
