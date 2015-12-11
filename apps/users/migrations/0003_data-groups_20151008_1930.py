# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import transaction
from django.db import migrations


def create_groups(apps, schema_editor):
    from django.contrib.auth.models import Group, Permission

    admin_group = Group.objects.create(name='SuperOwner')
    Group.objects.create(name='Owner')
    Group.objects.create(name='Accountant')

    all_permissions = Permission.objects.all()
    admin_group.permissions = all_permissions


def add_admin_user_to_admin_group(apps, schema_editor):
    from apps.users.models import User

    try:
        with transaction.atomic():
            admin = User.objects.get(username='admin')
        admin.add_to_group('Admin')
    except User.DoesNotExist:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_data-admin_20151007_1847'),
    ]

    operations = [
        migrations.RunPython(create_groups),
        # migrations.RunPython(add_admin_user_to_admin_group),
    ]
