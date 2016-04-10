# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import transaction
from django.db import migrations, IntegrityError


def create_admin(apps, schema_editor):
    from apps.users.models import User

    try:
        with transaction.atomic():
            User.objects.create_superuser('admin', 'webadmin@awecode.com', 'admin', full_name='admin')
    except IntegrityError:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]
