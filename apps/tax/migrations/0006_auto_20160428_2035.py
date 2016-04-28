# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0022_auto_20160428_2035'),
        ('tax', '0005_auto_20160306_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxscheme',
            name='ledger',
            field=models.ForeignKey(to='ledger.Account', null=True),
        ),
        migrations.AlterField(
            model_name='partytaxpreference',
            name='default_tax_application_type',
            field=models.CharField(default=b'inclusive', max_length=15, null=True, blank=True, choices=[(b'no', b'No Tax'), (b'inclusive', b'Tax Inclusive'), (b'exclusive', b'Tax Exclusive'), (b'no-preference', b'No Preference')]),
        ),
    ]
