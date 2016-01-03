from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from njango.fields import BSDateField, today

from django.db import models
from ..inventory.models import Item, Unit
from ..ledger.models import Party, Account
from ..users.models import Company
from awecounting.utils.helpers import get_next_voucher_no
from django.utils.translation import ugettext_lazy as _

class Purchase(models.Model):
    party = models.ForeignKey(Party)
    voucher_no = models.PositiveIntegerField(blank=True, null=True)
    credit = models.BooleanField(default=False)
    date = BSDateField(default=today)
    due_date = BSDateField(blank=True, null=True)
    company = models.ForeignKey(Company)

    def type(self):
        if self.credit:
            return _('Credit')
        else:
            return _('Cash')

    def clean(self):
        if self.company.settings.unique_voucher_number:
            if self.__class__.objects.filter(voucher_no=self.voucher_no).filter(
                    date__gte=self.company.settings.get_fy_start(self.date),
                    date__lte=self.company.settings.get_fy_end(self.date)).exclude(pk=self.pk):
                raise ValidationError(_('Voucher no. already exists for the fiscal year!'))

    def __init__(self, *args, **kwargs):
        super(Purchase, self).__init__(*args, **kwargs)

        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(Purchase, self.company_id)

    @property
    def total(self):
        grand_total = 0
        for obj in self.rows.all():
            total = obj.quantity * obj.rate
            grand_total += total
        return grand_total

    def get_absolute_url(self):
        return reverse_lazy('purchase-detail', kwargs={'id': self.pk})


class PurchaseRow(models.Model):
    sn = models.PositiveIntegerField()
    item = models.ForeignKey(Item)
    quantity = models.FloatField()
    rate = models.FloatField()
    discount = models.FloatField(default=0)
    unit = models.ForeignKey(Unit)
    purchase = models.ForeignKey(Purchase, related_name='rows')

    def get_voucher_no(self):
        return self.purchase.voucher_no

    def get_absolute_url(self):
        return reverse_lazy('purchase-detail', kwargs={'id': self.purchase.pk})


class Sale(models.Model):
    party = models.ForeignKey(Party, blank=True, null=True)
    credit = models.BooleanField(default=False)
    voucher_no = models.PositiveIntegerField(blank=True, null=True)
    date = BSDateField(default=today)
    due_date = BSDateField(blank=True, null=True)
    pending_amount = models.FloatField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    company = models.ForeignKey(Company)
    description = models.TextField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(Sale, self).__init__(*args, **kwargs)

        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(Sale, self.company)

    def clean(self):
        if self.company.settings.unique_voucher_number:
            if self.__class__.objects.filter(voucher_no=self.voucher_no).filter(
                    date__gte=self.company.settings.get_fy_start(self.date),
                    date__lte=self.company.settings.get_fy_end(self.date)).exclude(pk=self.pk):
                raise ValidationError(_('Voucher no. already exists for the fiscal year!'))

    def get_absolute_url(self):
        return reverse_lazy('sale-detail', kwargs={'id': self.pk})

    def type(self):
        if self.credit:
            return _('Credit')
        else:
            return _('Cash')

    @property
    def total(self):
        grand_total = 0
        for obj in self.rows.all():
            total = obj.quantity * obj.rate - obj.discount
            grand_total += total
        return grand_total


class SaleRow(models.Model):
    sn = models.PositiveIntegerField()
    item = models.ForeignKey(Item)
    quantity = models.FloatField()
    rate = models.FloatField()
    discount = models.FloatField(default=0)
    unit = models.ForeignKey(Unit)
    sale = models.ForeignKey(Sale, related_name='rows')

    def get_total(self):
        return float(self.quantity) * float(self.rate) - float(self.discount)

    def get_voucher_no(self):
        return self.sale.voucher_no

    def get_absolute_url(self):
        return reverse_lazy('sale-detail', kwargs={'id': self.sale.pk})


class JournalVoucher(models.Model):
    voucher_no = models.IntegerField()
    date = BSDateField(default=today)
    company = models.ForeignKey(Company)
    narration = models.TextField()
    statuses = [('Cancelled', 'Cancelled'), ('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __init__(self, *args, **kwargs):
        super(JournalVoucher, self).__init__(*args, **kwargs)

        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(JournalVoucher, self.company_id)

    def get_voucher_no(self):
        return self.voucher_no


class JournalVoucherRow(models.Model):
    types = [('Dr', 'Dr'), ('Cr', 'Cr')]
    type = models.CharField(choices=types, default='Dr', max_length=2)
    account = models.ForeignKey(Account, related_name='account_rows')
    description = models.TextField(null=True, blank=True)
    dr_amount = models.FloatField(null=True, blank=True)
    cr_amount = models.FloatField(null=True, blank=True)
    journal_voucher = models.ForeignKey(JournalVoucher, related_name='rows')

    def get_voucher_no(self):
        return self.journal_voucher.voucher_no



class CashReceipt(models.Model):
    voucher_no = models.IntegerField()
    party = models.ForeignKey(Party, verbose_name=_('Receipt From'))
    date = BSDateField(default=today)
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
