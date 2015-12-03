# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def initialize(apps, schema_editor):
	# Unit = apps.get_model('inventory', 'Unit')
	from apps.inventory import Unit
	Unit.objects.create(name="test")

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_auto_20150926_1438'),
    ]

    operations = [
    	migrations.RunPython(initialize),
    ]
