# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20151229_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.FileField(null=True, upload_to=b'cheque_payments/%Y/%m/%d', blank=True)),
                ('description', models.TextField(max_length=254, null=True, blank=True)),
            ],
        ),
    ]
