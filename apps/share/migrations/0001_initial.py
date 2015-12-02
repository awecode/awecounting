# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.date.today)),
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
            ],
        ),
        migrations.AddField(
            model_name='investment',
            name='share_holder',
            field=models.ForeignKey(to='share.ShareHolder'),
        ),
    ]
