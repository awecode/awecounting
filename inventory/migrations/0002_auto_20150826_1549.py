# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaserow',
            old_name='product',
            new_name='purchase',
        ),
        migrations.AddField(
            model_name='item',
            name='other_properties',
            field=jsonfield.fields.JSONField(null=True, blank=True),
        ),
    ]
