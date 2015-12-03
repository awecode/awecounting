# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20150827_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description_en',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='description_ne',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='name_en',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='name_ne',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='party',
            name='name_en',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='party',
            name='name_ne',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='name_en',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='name_ne',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
