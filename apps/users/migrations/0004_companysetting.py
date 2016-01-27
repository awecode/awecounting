# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import njango.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_data-groups_20151008_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanySetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voucher_number_start_date', njango.fields.BSDateField(default=njango.fields.today)),
                ('voucher_number_restart_years', models.IntegerField(default=1)),
                ('voucher_number_restart_months', models.IntegerField(default=0)),
                ('voucher_number_restart_days', models.IntegerField(default=0)),
                ('company', models.OneToOneField(related_name='settings', to='users.Company')),
            ],
        ),
    ]
