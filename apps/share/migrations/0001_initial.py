# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveIntegerField()),
                ('interest_rate', models.FloatField()),
                ('start_date', njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True)),
                ('end_date', njango.fields.BSDateField(default=njango.fields.today, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', njango.fields.BSDateField(default=njango.fields.today)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ShareHolder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('phone_no', models.CharField(max_length=50, null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('account', models.ForeignKey(to='ledger.Account', null=True)),
            ],
        ),
    ]
