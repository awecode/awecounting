import datetime
from django.core.exceptions import ValidationError
from njango.fields import BSDateField, today
from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse_lazy
from django.db import models
from jsonfield import JSONField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import F
from ..ledger.models import Account
from ..users.models import Company
from awecounting.utils.helpers import get_next_voucher_no, none_for_zero, zero_for_none


class Unit(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10, blank=True, null=True)
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.name


class UnitConverter(models.Model):
    base_unit = models.ForeignKey(Unit, null=True, related_name='base_unit')
    unit_to_convert = models.ForeignKey(Unit, null=True)
    multiple = models.FloatField()

    def __unicode__(self):
        return self.unit_to_convert.name + ' ' + '[' + str(self.multiple) + ':' + self.base_unit.name + ']'


class InventoryAccount(models.Model):
    # code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100)
    account_no = models.PositiveIntegerField()
    current_balance = models.FloatField(default=0)
    company = models.ForeignKey(Company)

    def __str__(self):
        return str(self.account_no) + ' [' + self.name + ']'

    def get_absolute_url(self):
        return '/inventory_account/' + str(self.id)

    @staticmethod
    def get_next_account_no():
        from django.db.models import Max

        max_voucher_no = InventoryAccount.objects.all().aggregate(Max('account_no'))['account_no__max']
        if max_voucher_no:
            return max_voucher_no + 1
        else:
            return 1


class Item(models.Model):
    code = models.CharField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    account = models.OneToOneField(InventoryAccount, related_name='item', null=True)
    image = models.ImageField(upload_to='items', blank=True, null=True)
    size = models.CharField(max_length=250, blank=True, null=True)
    unit = models.ForeignKey(Unit, related_name="item_unit", blank=False, null=True, on_delete=models.SET_NULL)
    selling_rate = models.FloatField(blank=True, null=True)
    other_properties = JSONField(blank=True, null=True)
    ledger = models.ForeignKey(Account, null=True)
    company = models.ForeignKey(Company)

    def __str__(self):
        return str(self.name) + ' ' + str(self.code)

    def save(self, *args, **kwargs):
        account_no = kwargs.pop('account_no')

        if not self.ledger_id:
            ledger = Account(name=self.name, company=self.company)
            ledger.save()
            self.ledger = ledger

        if account_no:
            if self.account:
                account = self.account
                account.account_no = account_no
                account.company = self.company
            else:
                account = InventoryAccount(name=self.name, account_no=account_no, company=self.company)
                account.save()
                self.account = account
        super(Item, self).save(*args, **kwargs)


class JournalEntry(models.Model):
    date = models.DateField()
    content_type = models.ForeignKey(ContentType, related_name='inventory_journal_entries')
    model_id = models.PositiveIntegerField()
    creator = GenericForeignKey('content_type', 'model_id')

    @staticmethod
    def get_for(source):
        try:
            return JournalEntry.objects.get(content_type=ContentType.objects.get_for_model(source), model_id=source.id)
        except JournalEntry.DoesNotExist:
            return None

    def __str__(self):
        return str(self.content_type) + ': ' + str(self.model_id) + ' [' + str(self.date) + ']'

    class Meta:
        verbose_name_plural = u'InventoryJournal Entries'


class Transaction(models.Model):
    account = models.ForeignKey(InventoryAccount)
    dr_amount = models.FloatField(null=True, blank=True)
    cr_amount = models.FloatField(null=True, blank=True)
    current_balance = models.FloatField(null=True, blank=True)
    journal_entry = models.ForeignKey(JournalEntry, related_name='transactions')

    def __str__(self):
        return str(self.account) + ' [' + str(self.dr_amount) + ' / ' + str(self.cr_amount) + ']'


def alter(account, date, diff):
    Transaction.objects.filter(journal_entry__date__gt=date, account=account).update(
        current_balance=none_for_zero(zero_for_none(F('current_balance')) + zero_for_none(diff)))


def set_transactions(model, date, *args):
    args = [arg for arg in args if arg is not None]
    journal_entry, created = JournalEntry.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(model), model_id=model.id,
        defaults={
            'date': date
        })

    for arg in args:
        matches = journal_entry.transactions.filter(account=arg[1])
        diff = 0
        if not matches:
            transaction = Transaction()
        else:
            transaction = matches[0]
            diff = zero_for_none(transaction.cr_amount)
            diff -= zero_for_none(transaction.dr_amount)
        if arg[0] == 'dr':
            transaction.dr_amount = float(arg[2])
            transaction.cr_amount = None
            diff += float(arg[2])
        elif arg[0] == 'cr':
            transaction.cr_amount = float(arg[2])
            transaction.dr_amount = None
            diff -= float(arg[2])
        else:
            raise Exception('Transactions can only be either "dr" or "cr".')
        transaction.account = arg[1]
        transaction.account.current_balance += diff
        transaction.current_balance = transaction.account.current_balance
        transaction.account.save()
        journal_entry.transactions.add(transaction)
        alter(transaction.account, date, diff)


class Party(models.Model):
    name = models.CharField(max_length=254)
    address = models.CharField(max_length=254, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    pan_no = models.CharField(max_length=50, blank=True, null=True)
    account = models.ForeignKey(Account, null=True)
    company = models.ForeignKey(Company)

    # def clean(self):
    #     if self.pan_no:
    #         conflicting_instance = Party.objects.filter(pan_no=self.pan_no, company=self.company).exclude(pk=self.pk)
    #         if conflicting_instance.exists():
    #             raise forms.ValidationError(_('Company with this PAN already exists.'))

    def get_absolute_url(self):
        return reverse_lazy('party_edit', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.account_id:
            account = Account(name=self.name, company=self.company)
            account.save()
            self.account = account

        super(Party, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Parties'
        # unique_together = ['pan_no', 'company']


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
