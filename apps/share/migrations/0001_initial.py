# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveIntegerField()),
                ('interest_rate', models.FloatField()),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.FloatField()),
                ('collection', models.ForeignKey(to='share.Collection')),
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
                ('company', models.ForeignKey(to='users.Company')),
            ],
        ),
        migrations.AddField(
            model_name='investment',
            name='share_holder',
            field=models.ForeignKey(to='share.ShareHolder'),
        ),
    ]
