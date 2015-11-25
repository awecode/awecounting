# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def initializ(apps, schema_editor):
	# Unit = apps.get_model('inventory', 'Unit')
	from inventory.models import Unit
	Unit.objects.create(name="roshan")
	Unit.objects.create(name="roshan")
	Unit.objects.create(name="roshan")

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_auto_20150926_1438'),
    ]

    operations = [
    	migrations.RunPython(initializ),
    ]
