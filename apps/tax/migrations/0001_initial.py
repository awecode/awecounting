# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20160124_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxScheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=5, null=True, blank=True)),
                ('percent', models.FloatField()),
                ('recoverable', models.FloatField(default=False)),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
    ]
