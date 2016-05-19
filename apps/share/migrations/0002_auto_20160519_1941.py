# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shareholder',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='investment',
            name='collection',
            field=models.ForeignKey(to='share.Collection'),
        ),
        migrations.AddField(
            model_name='investment',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='investment',
            name='share_holder',
            field=models.ForeignKey(to='share.ShareHolder'),
        ),
        migrations.AddField(
            model_name='collection',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
    ]
