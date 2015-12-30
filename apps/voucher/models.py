from __future__ import unicode_literals

from django.db import models
from ..inventory.models import Party, Sale
from ..users.models import Company
from awecounting.utils.helpers import get_next_voucher_no


class CashReceipt(models.Model):
    voucher_no = models.IntegerField()
    party = models.ForeignKey(Party, verbose_name='Receipt From')
    receipt_on = models.DateField()
    reference = models.CharField(max_length=50, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    description = models.TextField()
    company = models.ForeignKey(Company)
    # statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    # status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __init__(self, *args, **kwargs):
        super(CashReceipt, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(CashReceipt, self.company)


class CashReceiptRow(models.Model):
    invoice = models.ForeignKey(Sale, related_name='receipts')
    receipt = models.FloatField()
    discount = models.FloatField()
    cash_receipt = models.ForeignKey(CashReceipt, related_name='rows')
