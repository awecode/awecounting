# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PartyTaxPreference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_tax_application_type', models.CharField(default=b'inclusive', max_length=15, null=True, blank=True, choices=[(b'no', b'No Tax'), (b'inclusive', b'Tax Inclusive'), (b'exclusive', b'Tax Exclusive'), (b'no-preference', b'No Preference')])),
            ],
        ),
        migrations.CreateModel(
            name='TaxScheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=5, null=True, blank=True)),
                ('percent', models.FloatField()),
                ('recoverable', models.BooleanField(default=False)),
            ],
        ),
    ]
