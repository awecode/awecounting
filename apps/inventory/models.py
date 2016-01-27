from django.db import models
from jsonfield import JSONField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import F, Q
from ..ledger.models import Account
from ..users.models import Company
from awecounting.utils.helpers import none_for_zero, zero_for_none
from ..users.signals import company_creation
from django.dispatch import receiver


class Unit(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10, blank=True, null=True)
    company = models.ForeignKey(Company)

    def get_base_conversions(self, exclude=None):
        return self.base_conversions.all()

    def get_conversions(self, exclude=None):
        return self.conversions.all()

    def get_all_conversions(self, exclude=[]):

        base_conversions = UnitConversion.objects.filter(base_unit=self).exclude(pk__in=exclude)
        conversions = UnitConversion.objects.filter(unit_to_convert=self).exclude(pk__in=exclude)
        ret = []
        for base_conversion in base_conversions:
            ret.append(base_conversion)
        for conversion in conversions:
            conversion.multiple = 1 / conversion.multiple
            ret.append(conversion)
        return ret

        qs = UnitConversion.objects.filter(base_unit=self).extra(
            select={'multiple': '1 / multiple'}) | UnitConversion.objects.filter(
            unit_to_convert=self)
        return qs.exclude(pk__in=exclude)

    def convertibles(self):
        def find_convertibles(data, exclude, mul, base_unit=None):
            # print ''
            if not base_unit:
                base_unit = self
            # print 'Convertible for ' + str(base_unit)
            # print 'Passed multiple is ' + str(mul)
            if base_unit.id not in data.keys():
                data[base_unit.id] = mul
                # print data
                # print 'Exclude: ' + str(exclude)
                # print 'Conversions: ' + str(base_unit.get_all_conversions(exclude))
                for conversion in base_unit.get_all_conversions(exclude):
                    exclude.append(conversion.pk)
                    unit = conversion.get_another_unit(base_unit.id)
                    # print '\nConverting to ' + str(unit) + ' with multiple ' + str(conversion.multiple * mul)
                    for key, val in find_convertibles(data, exclude, conversion.multiple * mul, unit).items():
                        if not key in data.keys():
                            # print 'writing: ' + str(key) + ' : ' + str(val)
                            data[key] = val * conversion.multiple
            return data
        all_convertibles = find_convertibles({}, [], 1)
        all_convertibles.pop(self.id, None)
        return all_convertibles

        # for conversion in self.get_conversions():
        #     if conversion.base_unit_id not in data.keys():
        #         for key, val in conversion.base_unit.convertibles(data).items():
        #             data[key] = val / conversion.multiple
        #     data[conversion.base_unit_id] = 1 / conversion.multiple
        # return data

    def __unicode__(self):
        return self.name


@receiver(company_creation)
def handle_company_creation(sender, **kwargs):
    company = kwargs.get('company')
    Unit.objects.create(name="Pieces", short_name='pcs', company=company)


class UnitConversion(models.Model):
    base_unit = models.ForeignKey(Unit, null=True, related_name='base_conversions')
    unit_to_convert = models.ForeignKey(Unit, null=True, related_name='conversions')
    multiple = models.FloatField()
    company = models.ForeignKey(Company)

    def get_another_unit(self, unit_id):
        if unit_id == self.base_unit_id:
            return self.unit_to_convert
        return self.base_unit

    def __unicode__(self):
        return self.base_unit.name + ' - ' + self.unit_to_convert.name + ' : ' + str(self.multiple)


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
