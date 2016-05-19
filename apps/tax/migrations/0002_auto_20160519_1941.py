# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0001_initial'),
        ('ledger', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxscheme',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='partytaxpreference',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='partytaxpreference',
            name='party',
            field=models.OneToOneField(related_name='tax_preference', to='ledger.Party'),
        ),
        migrations.AddField(
            model_name='partytaxpreference',
            name='tax_scheme',
            field=models.ForeignKey(blank=True, to='tax.TaxScheme', null=True),
        ),
    ]
