from __future__ import unicode_literals

from datetime import date

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey

from njango.fields import BSDateField, today
from ..inventory.models import Item, Unit
from ..ledger.models import Party, Account, JournalEntry
from ..users.models import Company, User
from awecounting.utils.helpers import get_next_voucher_no, calculate_tax
from ..tax.models import TaxScheme
from awecounting.utils.helpers import get_discount_with_percent
from ..users.signals import company_creation




class PurchaseVoucher(models.Model):
    tax_choices = [('no', 'No Tax'), ('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'), ]
    party = models.ForeignKey(Party)
    voucher_no = models.PositiveIntegerField(blank=True, null=True)
    credit = models.BooleanField(default=False)
    date = BSDateField(default=today)
    tax = models.CharField(max_length=10, choices=tax_choices, default='inclusive', null=True, blank=True)
    tax_scheme = models.ForeignKey(TaxScheme, blank=True, null=True)
    due_date = BSDateField(blank=True, null=True)
    pending_amount = models.FloatField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    company = models.ForeignKey(Company)
    discount = models.CharField(max_length=50, blank=True, null=True)

    def type(self):
        if self.credit:
            return _('Credit')
        else:
            return _('Cash')

    def clean(self):
        if self.company.settings.unique_voucher_number:
            if self.__class__.objects.filter(voucher_no=self.voucher_no, company=self.company).filter(
                    date__gte=self.company.get_fy_start(self.date),
                    date__lte=self.company.get_fy_end(self.date)).exclude(pk=self.pk):
                raise ValidationError(_('Voucher no. already exists for the fiscal year!'))

    def __init__(self, *args, **kwargs):
        super(PurchaseVoucher, self).__init__(*args, **kwargs)

        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(PurchaseVoucher, self.company_id)

    @property
    def sub_total(self):
        grand_total = 0
        for obj in self.rows.all():
            total = obj.quantity * obj.rate
            discount = get_discount_with_percent(total, obj.discount)
            grand_total += total - discount
        return grand_total

    @property
    def tax_amount(self):
        _sum = 0
        if self.tax_scheme:
            _sum = calculate_tax(self.tax, self.sub_total, self.tax_scheme.percent)
        else:
            for obj in self.rows.all():
                if obj.tax_scheme:
                    total = obj.quantity * obj.rate - float(obj.discount)
                    amount = calculate_tax(self.tax, total, obj.tax_scheme.percent)
                    _sum += amount
        return _sum

    @property
    def total(self):
        amount = self.sub_total
        if self.tax == "exclusive":
            amount = self.sub_total + self.tax_amount
        if self.discount:
            discount = get_discount_with_percent(amount, self.discount)
            amount = amount - discount
        return amount

    @property
    def voucher_type(self):
        return _('PurchaseVoucher')

    @property
    def row_discount_total(self):
        grand_total = 0
        for obj in self.rows.all():
            total = obj.quantity * obj.rate
            discount = get_discount_with_percent(total, obj.discount)
            grand_total += discount
        return grand_total

    def get_absolute_url(self):
        return reverse_lazy('purchase-edit', kwargs={'pk': self.pk})


class LotItemDetail(models.Model):
    item = models.ForeignKey(Item)
    qty = models.PositiveIntegerField()
    # po_receive_lot = models.ForeignKey(PoReceiveLot)

    def __unicode__(self):
        return '%s-QTY#%d' % (self.item, self.qty)


class Lot(models.Model):
    lot_number = models.CharField(max_length=150, unique=True)
    lot_item_details = models.ManyToManyField(
        LotItemDetail
    )

    def __unicode__(self):
        return self.lot_number


class PurchaseVoucherRow(models.Model):
    sn = models.PositiveIntegerField()
    item = models.ForeignKey(Item, related_name='purchases')
    quantity = models.FloatField()
    rate = models.FloatField()
    discount = models.CharField(max_length=50, blank=True, null=True)
    tax_scheme = models.ForeignKey(TaxScheme, blank=True, null=True)
    unit = models.ForeignKey(Unit)
    purchase = models.ForeignKey(PurchaseVoucher, related_name='rows')
    journal_entry = GenericRelation(JournalEntry)
    lot = models.ForeignKey(Lot, null=True, blank=True)

    def get_total(self):
        total = float(self.quantity) * float(self.rate)
        discount = get_discount_with_percent(total, self.discount)
        return total - discount

    def get_voucher_no(self):
        return self.purchase.voucher_no

    def get_absolute_url(self):
        return reverse_lazy('purchase-edit', kwargs={'pk': self.purchase.pk})

    @property
    def voucher_type(self):
        return _('PurchaseVoucher')


class TradeExpense(models.Model):
    expense = models.ForeignKey(Account)
    amount = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.expense) + str(self.amount)


class PurchaseOrder(models.Model):
    party = models.ForeignKey(Party)
    voucher_no = models.IntegerField(blank=True, null=True)
    date = BSDateField(default=today)
    purchase_agent = models.ForeignKey(User, related_name="purchase_order", blank=True, null=True)
    trade_expense = GenericRelation(TradeExpense)
    company = models.ForeignKey(Company)

    def __init__(self, *args, **kwargs):
        super(PurchaseOrder, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(PurchaseOrder, self.company_id)

    def __unicode__(self):
        return _('Purchase Order') + ' (' + str(self.voucher_no) + ')'

    @property
    def total(self):
        total = 0
        for obj in self.rows.all():
            total += obj.quantity * obj.rate
        return total


class PurchaseOrderRow(models.Model):
    sn = models.PositiveIntegerField()
    item = models.ForeignKey(Item)
    specification = models.CharField(max_length=254, blank=True, null=True)
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit)
    # unit = models.CharField(max_length=50)
    rate = models.FloatField(blank=True, null=True)
    # vattable = models.BooleanField(default=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    fulfilled = models.BooleanField(default=False)
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='rows')

    def get_total(self):
        total = 0
        if self.rate:
            total = float(self.quantity) * float(self.rate)
        return total


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
    tax_choices = [('no', 'No Tax'), ('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'), ]
    tax = models.CharField(max_length=10, choices=tax_choices, default='inclusive', null=True, blank=True)
    tax_scheme = models.ForeignKey(TaxScheme, blank=True, null=True)
    discount = models.CharField(max_length=50, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(Sale, self).__init__(*args, **kwargs)

        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(Sale, self.company)

    def clean(self):
        if self.company.settings.unique_voucher_number:
            pass
            # if self.__class__.objects.filter(voucher_no=self.voucher_no, company=self.company).filter(
            #       date__gte=self.company.settings.get_fy_start(self.date),
            #       date__lte=self.company.settings.get_fy_end(self.date)).exclude(pk=self.pk):
            #   raise ValidationError(_('Voucher no. already exists for the fiscal year!'))

    def get_absolute_url(self):
        return reverse_lazy('sale-edit', kwargs={'pk': self.pk})

    def type(self):
        if self.credit:
            return _('Credit')
        else:
            return _('Cash')

    def __str__(self):
        return str(self.voucher_no)

    @property
    def voucher_type(self):
        return _('Sale')

    @property
    def sub_total(self):
        grand_total = 0
        for obj in self.rows.all():
            total = obj.quantity * obj.rate
            discount = get_discount_with_percent(total, obj.discount)
            grand_total += total - discount
        return grand_total

    @property
    def tax_amount(self):
        _sum = 0
        if self.tax_scheme:
            _sum = calculate_tax(self.tax, self.sub_total, self.tax_scheme.percent)
        else:
            for obj in self.rows.all():
                if obj.tax_scheme:
                    total = obj.quantity * obj.rate - float(obj.discount)
                    amount = calculate_tax(self.tax, total, obj.tax_scheme.percent)
                    _sum += amount
        return _sum

    @property
    def total(self):
        amount = self.sub_total
        if self.tax == "exclusive":
            amount = self.sub_total + self.tax_amount
        if self.discount:
            discount = get_discount_with_percent(amount, self.discount)
            amount = amount - discount
        return amount


class SaleRow(models.Model):
    sn = models.PositiveIntegerField()
    item = models.ForeignKey(Item, related_name='sales')
    quantity = models.FloatField()
    rate = models.FloatField()
    discount = models.FloatField(default=0)
    unit = models.ForeignKey(Unit)
    sale = models.ForeignKey(Sale, related_name='rows')
    tax_scheme = models.ForeignKey(TaxScheme, blank=True, null=True)
    journal_entry = GenericRelation(JournalEntry)

    def get_total(self):
        return float(self.quantity) * float(self.rate) - float(self.discount)

    def get_voucher_no(self):
        return self.sale.voucher_no

    @property
    def voucher_type(self):
        return _('Sale')

    def get_absolute_url(self):
        return reverse_lazy('sale-edit', kwargs={'pk': self.sale.pk})


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

    def get_total_dr_amount(self):
        total_dr_amount = 0
        for o in self.rows.all():
            total_dr_amount += o.dr_amount
        return total_dr_amount

    def get_total_cr_amount(self):
        total_cr_amount = 0
        for o in self.rows.all():
            total_cr_amount += o.cr_amount
        return total_cr_amount

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
            self.voucher_no = get_next_voucher_no(CashReceipt, self.company_id)

    @property
    def total(self):
        grand_total = 0
        for obj in self.rows.all():
            total = obj.receipt
            grand_total += total
        return grand_total

    def get_voucher_no(self):
        return self.voucher_no

    def get_absolute_url(self):
        return reverse_lazy('cash_receipt_edit', kwargs={'pk': self.pk})


class CashReceiptRow(models.Model):
    invoice = models.ForeignKey(Sale, related_name='receipts')
    receipt = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    cash_receipt = models.ForeignKey(CashReceipt, related_name='rows')

    def get_voucher_no(self):
        return self.cash_receipt.voucher_no

    def get_absolute_url(self):
        return reverse_lazy('cash_receipt_edit', kwargs={'pk': self.cash_receipt_id})

    def overdue_days(self):
        if self.invoice.due_date and self.invoice.due_date < date.today():
            overdue_days = date.today() - self.invoice.due_date
            return overdue_days.days
        return ''

    class Meta:
        unique_together = ('invoice', 'cash_receipt')


class CashPayment(models.Model):
    voucher_no = models.IntegerField()
    party = models.ForeignKey(Party, verbose_name='Paid To')
    date = BSDateField(default=today)
    reference = models.CharField(max_length=50, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    description = models.TextField()
    company = models.ForeignKey(Company)
    # statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    # status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __init__(self, *args, **kwargs):
        super(CashPayment, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(CashPayment, self.company_id)

    @property
    def total(self):
        grand_total = 0
        for obj in self.rows.all():
            total = obj.payment
            grand_total += total
        return grand_total

    def get_voucher_no(self):
        return self.voucher_no

    def get_absolute_url(self):
        return reverse_lazy('cash_payment_edit', kwargs={'pk': self.pk})


class CashPaymentRow(models.Model):
    invoice = models.ForeignKey(PurchaseVoucher, related_name="receipts")
    payment = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    cash_payment = models.ForeignKey(CashPayment, related_name='rows')

    def get_voucher_no(self):
        return self.cash_payment.voucher_no

    def get_absolute_url(self):
        return reverse_lazy('cash_payment_edit', kwargs={'pk': self.cash_payment_id})

    def overdue_days(self):
        if self.invoice.due_date and self.invoice.due_date < date.today():
            overdue_days = date.today() - self.invoice.due_date
            return overdue_days.days
        return ''

    class Meta:
        unique_together = ('invoice', 'cash_payment')


class FixedAsset(models.Model):
    from_account = models.ForeignKey(Account)
    voucher_no = models.IntegerField()
    date = BSDateField(default=today)
    reference = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company)
    # statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    # status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __init__(self, *args, **kwargs):
        super(FixedAsset, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(FixedAsset, self.company_id)

    @property
    def total(self):
        grand_total = 0
        for obj in self.rows.all():
            total = obj.amount
            grand_total += total
        return grand_total


class FixedAssetRow(models.Model):
    asset_ledger = models.ForeignKey(Account)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    fixed_asset = models.ForeignKey(FixedAsset, related_name='rows')


class AdditionalDetail(models.Model):
    assets_code = models.CharField(max_length=100, null=True, blank=True)
    assets_type = models.CharField(max_length=100, null=True, blank=True)
    vendor_name = models.CharField(max_length=100, null=True, blank=True)
    vendor_address = models.CharField(max_length=254, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    useful_life = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    warranty_period = models.CharField(max_length=100, null=True, blank=True)
    maintenance = models.CharField(max_length=100, null=True, blank=True)
    fixed_asset = models.ForeignKey(FixedAsset, related_name='additional_details')


class VoucherSetting(models.Model):
    # from ..tax.models import TaxScheme
    tax_choices = [('no', 'No Tax'), ('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'), ]
    company = models.OneToOneField(Company, related_name='settings')
    unique_voucher_number = models.BooleanField(default=True)
    single_discount_on_whole_invoice = models.BooleanField(default=True)
    discount_on_each_invoice_particular = models.BooleanField(default=False)
    sale_default_tax_application_type = models.CharField(max_length=10, choices=tax_choices, default='exclusive',
                                                         null=True,
                                                         blank=True)
    sale_default_tax_scheme = models.ForeignKey(TaxScheme, blank=True, null=True,
                                                related_name="default_invoice_tax_scheme")

    single_discount_on_whole_purchase = models.BooleanField(default=True)
    discount_on_each_purchase_particular = models.BooleanField(default=False)
    purchase_default_tax_application_type = models.CharField(max_length=10, choices=tax_choices, default='exclusive',
                                                             null=True,
                                                             blank=True)
    purchase_default_tax_scheme = models.ForeignKey(TaxScheme, blank=True, null=True,
                                                    related_name="default_purchase_tax_scheme")
    purchase_suggest_by_item = models.BooleanField(default=True, verbose_name='Suggest rate by item')
    purchase_suggest_by_party_item = models.BooleanField(default=True, verbose_name='Suggest rate by item by party')
    sale_suggest_by_item = models.BooleanField(default=True, verbose_name='Suggest rate by item')
    sale_suggest_by_party_item = models.BooleanField(default=True, verbose_name='Suggest rate by item by party')
    enable_expense_in_purchase = models.BooleanField(default=True, verbose_name='Enable Expense')
    add_expense_cost_to_purchase = models.BooleanField(default=True, verbose_name='Add expense cost')

    def __unicode__(self):
        return self.company.name


@receiver(company_creation)
def handle_company_creation(sender, **kwargs):
    company = kwargs.get('company')
    VoucherSetting.objects.create(company=company)


class Expense(models.Model):
    voucher_no = models.IntegerField(blank=True, null=True)
    date = BSDateField(default=today)
    company = models.ForeignKey(Company)

    def __init__(self, *args, **kwargs):
        super(Expense, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(Expense, self.company_id)

    @property
    def total(self):
        grand_total = 0
        for obj in self.rows.all():
            total = obj.amount
            grand_total += total
        return grand_total


class ExpenseRow(models.Model):
    expense = models.ForeignKey(Account, related_name="expense")
    pay_head = models.ForeignKey(Account, related_name="cash_and_bank")
    amount = models.IntegerField()
    expense_row = models.ForeignKey(Expense, related_name="rows")
