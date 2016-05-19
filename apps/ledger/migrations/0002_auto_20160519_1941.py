# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0001_initial'),
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='company',
            field=models.ForeignKey(related_name='parties', to='users.Company'),
        ),
        migrations.AddField(
            model_name='party',
            name='customer_ledger',
            field=models.OneToOneField(related_name='customer_detail', null=True, to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='party',
            name='related_company',
            field=models.OneToOneField(related_name='related_party', null=True, blank=True, to='users.Company'),
        ),
        migrations.AddField(
            model_name='party',
            name='supplier_ledger',
            field=models.OneToOneField(related_name='supplier_detail', null=True, to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='category',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', blank=True, to='ledger.Category', null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='category',
            field=models.ForeignKey(related_name='accounts', blank=True, to='ledger.Category', null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='account',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='ledger.Account', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='party',
            unique_together=set([('company', 'related_company')]),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('name', 'company')]),
        ),
    ]
