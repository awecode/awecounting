# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def initializ(apps, schema_editor):
	# Unit = apps.get_model('inventory', 'Unit')
	from apps.inventory import Unit
	Unit.objects.create(name="roshan")
	Unit.objects.create(name="roshan")
	Unit.objects.create(name="roshan")

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0022_auto_20151008_1046'),
        ('inventory', '0021_auto_20151008_1043'),
    ]

    operations = [
    	migrations.RunPython(initializ),
    ]
