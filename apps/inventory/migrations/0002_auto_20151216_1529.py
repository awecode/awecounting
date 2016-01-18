# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
        ('users', '0003_data-groups_20151008_1930'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='account',
            field=models.ForeignKey(to='ledger.Account', null=True),
        ),
        migrations.AddField(
            model_name='party',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='content_type',
            field=models.ForeignKey(related_name='inventory_journal_entries', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='item',
            name='account',
            field=models.OneToOneField(related_name='item', null=True, to='inventory.InventoryAccount'),
        ),
        migrations.AddField(
            model_name='item',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='item',
            name='ledger',
            field=models.ForeignKey(to='ledger.Account', null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(to='inventory.Unit'),
        ),
        migrations.AddField(
            model_name='inventoryaccount',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
    ]
