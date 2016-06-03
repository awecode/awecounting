# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0035_purchaseorderrow_fulfilled'),
    ]

    operations = [
        migrations.CreateModel(
            name='PoReceiveLot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lot_number', models.CharField(unique=True, max_length=150)),
            ],
        ),
    ]
