# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-05 10:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_company_tax_registration_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pin', to='users.Company')),
                ('used_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='used_pin', to='users.Company')),
            ],
        ),
    ]
