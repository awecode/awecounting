# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0001_initial'),
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitconversion',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='unitconversion',
            name='unit_to_convert',
            field=models.ForeignKey(related_name='conversions', to='inventory.Unit', null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(related_name='account_transaction', to='inventory.InventoryAccount'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='journal_entry',
            field=models.ForeignKey(related_name='transactions', to='inventory.JournalEntry'),
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
            name='purchase_ledger',
            field=models.OneToOneField(related_name='purchase_detail', null=True, to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='item',
            name='sale_ledger',
            field=models.OneToOneField(related_name='sale_detail', null=True, to='ledger.Account'),
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(related_name='item_unit', on_delete=django.db.models.deletion.SET_NULL, to='inventory.Unit', null=True),
        ),
        migrations.AddField(
            model_name='inventoryaccount',
            name='company',
            field=models.ForeignKey(to='users.Company'),
        ),
    ]
