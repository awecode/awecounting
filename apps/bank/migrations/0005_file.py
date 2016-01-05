# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0004_auto_20151228_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.FileField(null=True, upload_to=b'cheque_payments/%Y/%m/%d', blank=True)),
                ('narration', models.TextField(null=True, blank=True)),
                ('cheque_deposit', models.ForeignKey(related_name='file', to='bank.ChequeDeposit')),
            ],
        ),
    ]
