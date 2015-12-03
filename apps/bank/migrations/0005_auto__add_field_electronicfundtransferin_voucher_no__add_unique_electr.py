# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ElectronicFundTransferIn.voucher_no'
        db.add_column(u'bank_electronicfundtransferin', 'voucher_no',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding unique constraint on 'ElectronicFundTransferIn', fields ['voucher_no', 'company']
        db.create_unique(u'bank_electronicfundtransferin', ['voucher_no', 'company_id'])

        # Adding field 'ChequeDeposit.voucher_no'
        db.add_column(u'bank_chequedeposit', 'voucher_no',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'ChequeDeposit.status'
        db.add_column(u'bank_chequedeposit', 'status',
                      self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10),
                      keep_default=False)


        # Changing field 'ChequeDeposit.company'
        db.alter_column(u'bank_chequedeposit', 'company_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'], null=True))

        # Changing field 'ChequeDeposit.benefactor'
        db.alter_column(u'bank_chequedeposit', 'benefactor_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'], null=True))

        # Changing field 'ChequeDeposit.date'
        db.alter_column(u'bank_chequedeposit', 'date', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'ChequeDeposit.bank_account'
        db.alter_column(u'bank_chequedeposit', 'bank_account_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['ledger.Account']))
        # Adding unique constraint on 'ChequeDeposit', fields ['voucher_no', 'company']
        db.create_unique(u'bank_chequedeposit', ['voucher_no', 'company_id'])

        # Adding field 'BankCashDeposit.voucher_no'
        db.add_column(u'bank_bankcashdeposit', 'voucher_no',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding unique constraint on 'BankCashDeposit', fields ['voucher_no', 'company']
        db.create_unique(u'bank_bankcashdeposit', ['voucher_no', 'company_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'BankCashDeposit', fields ['voucher_no', 'company']
        db.delete_unique(u'bank_bankcashdeposit', ['voucher_no', 'company_id'])

        # Removing unique constraint on 'ChequeDeposit', fields ['voucher_no', 'company']
        db.delete_unique(u'bank_chequedeposit', ['voucher_no', 'company_id'])

        # Removing unique constraint on 'ElectronicFundTransferIn', fields ['voucher_no', 'company']
        db.delete_unique(u'bank_electronicfundtransferin', ['voucher_no', 'company_id'])

        # Deleting field 'ElectronicFundTransferIn.voucher_no'
        db.delete_column(u'bank_electronicfundtransferin', 'voucher_no')

        # Deleting field 'ChequeDeposit.voucher_no'
        db.delete_column(u'bank_chequedeposit', 'voucher_no')

        # Deleting field 'ChequeDeposit.status'
        db.delete_column(u'bank_chequedeposit', 'status')


        # Changing field 'ChequeDeposit.company'
        db.alter_column(u'bank_chequedeposit', 'company_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['users.Company']))

        # Changing field 'ChequeDeposit.benefactor'
        db.alter_column(u'bank_chequedeposit', 'benefactor_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['ledger.Account']))

        # Changing field 'ChequeDeposit.date'
        db.alter_column(u'bank_chequedeposit', 'date', self.gf('django.db.models.fields.DateField')(default=1))

        # Changing field 'ChequeDeposit.bank_account'
        db.alter_column(u'bank_chequedeposit', 'bank_account_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['ledger.Account']))
        # Deleting field 'BankCashDeposit.voucher_no'
        db.delete_column(u'bank_bankcashdeposit', 'voucher_no')


    models = {
        u'bank.bankaccount': {
            'Meta': {'object_name': 'BankAccount'},
            'ac_no': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ledger.Account']", 'unique': 'True'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'branch_name': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'bank.bankcashdeposit': {
            'Meta': {'unique_together': "(('voucher_no', 'company'),)", 'object_name': 'BankCashDeposit'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_deposits'", 'to': u"orm['ledger.Account']"}),
            'benefactor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'deposited_by': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'bank.chequedeposit': {
            'Meta': {'unique_together': "(('voucher_no', 'company'),)", 'object_name': 'ChequeDeposit'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cheque_deposits'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'benefactor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']", 'null': 'True', 'blank': 'True'}),
            'clearing_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deposited_by': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'bank.chequedepositrow': {
            'Meta': {'object_name': 'ChequeDepositRow'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'cheque_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cheque_deposit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['bank.ChequeDeposit']"}),
            'cheque_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'drawee_bank': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'drawee_bank_address': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'bank.chequepayment': {
            'Meta': {'object_name': 'ChequePayment'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cheque_payments'", 'to': u"orm['ledger.Account']"}),
            'beneficiary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'cheque_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'bank.electronicfundtransferin': {
            'Meta': {'unique_together': "(('voucher_no', 'company'),)", 'object_name': 'ElectronicFundTransferIn'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'electronic_fund_transfer_in'", 'to': u"orm['ledger.Account']"}),
            'benefactor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'clearing_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'bank.electronicfundtransferinrow': {
            'Meta': {'object_name': 'ElectronicFundTransferInRow'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'drawee_bank': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'drawee_bank_address': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'electronic_fund_transfer_in': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['bank.ElectronicFundTransferIn']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transaction_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'transaction_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'bank.electronicfundtransferout': {
            'Meta': {'object_name': 'ElectronicFundTransferOut'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'electronic_fund_transfer_out'", 'to': u"orm['ledger.Account']"}),
            'beneficiary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'transaction_number': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'ledger.account': {
            'Meta': {'unique_together': "(('company', 'name'), ('company', 'code'))", 'object_name': 'Account'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accounts'", 'blank': 'True', 'to': u"orm['ledger.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'current_cr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'current_dr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'opening_cr': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'opening_dr': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'tax_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'ledger.category': {
            'Meta': {'unique_together': "(('company', 'name'),)", 'object_name': 'Category'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['ledger.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['bank']