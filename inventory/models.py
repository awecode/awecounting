from django.db import models
import datetime
from jsonfield import JSONField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import F

def none_for_zero(obj):
    if not obj:
        return None
    else:
        return obj

def zero_for_none(obj):
    if obj is None:
        return 0
    else:
        return obj


class Unit(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

class InventoryAccount(models.Model):
    # code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100)
    account_no = models.PositiveIntegerField()
    current_balance = models.FloatField(default=0)
    # opening_balance = models.FloatField(default=0)

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

    # def get_category(self):
    #     try:
    #         item = self.item
    #     except:
    #         return None
    #     try:
    #         category = item.category
    #     except:
    #         return None
    #     return category

    # def add_category(self, category):
    #     category_instance, created = Category.objects.get_or_create(name=category)
    #     self.category = category_instance

    # def get_all_categories(self):
    #     return self.category.get_ancestors(include_self=True)

    # categories = property(get_all_categories)

class Item(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    account = models.OneToOneField(InventoryAccount, related_name='item', null=True)
    image = models.ImageField(upload_to='items', blank=True, null=True)
    size = models.CharField(max_length=250, blank=True, null=True)
    unit = models.ForeignKey(Unit)
    other_properties = JSONField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        account_no = kwargs.pop('account_no')
        if account_no:
            if self.account:
                account = self.account
                account.account_no = account_no
            else:
                # account = InventoryAccount(name=self.name, account_no=account_no,
                #                            opening_balance=opening_balance, current_balance=opening_balance)
                account = InventoryAccount(name=self.name, account_no=account_no)
                account.save()
                self.account = account
        super(Item, self).save(*args, **kwargs)

class JournalEntry(models.Model):
    date = models.DateField()
    content_type = models.ForeignKey(ContentType, related_name='inventory_journal_entries')
    model_id = models.PositiveIntegerField()
    creator = GenericForeignKey('content_type', 'model_id')
    # country_of_production = models.CharField(max_length=50, blank=True, null=True)
    # size = models.CharField(max_length=100, blank=True, null=True)
    # expected_life = models.CharField(max_length=100, blank=True, null=True)
    # source = models.CharField(max_length=100, blank=True, null=True)

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

    # def total_dr_amount(self):
    #     dr_transctions = Transaction.objects.filter(account__name=self.account.name, cr_amount=None,
    #                                                 journal_entry__journal__rate=self.journal_entry.creator.rate)
    #     total = 0
    #     for transaction in dr_transctions:
    #         total += transaction.dr_amount
    #     return total

    # def total_dr_amount_without_rate(self):
    #     dr_transctions = Transaction.objects.filter(account__name=self.account.name, cr_amount=None)
    #     total = 0
    #     for transaction in dr_transctions:
    #         total += transaction.dr_amount
    #     return total


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

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Parties'

class Purchase(models.Model):
    party = models.ForeignKey(Party)
    voucher_no = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(default=datetime.datetime.today)

class PurchaseRow(models.Model):
    sn = models.PositiveIntegerField()
    item = models.ForeignKey(Item)
    quantity = models.FloatField()
    rate = models.FloatField()
    discount = models.FloatField(default=0)
    unit = models.ForeignKey(Unit)
    purchase = models.ForeignKey(Purchase, related_name='rows')

class Sale(models.Model):
    party = models.ForeignKey(Party, blank=True, null=True)
    voucher_no = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(default=datetime.datetime.today)

class SaleRow(models.Model):
    sn = models.PositiveIntegerField()
    item = models.ForeignKey(Item)
    quantity = models.FloatField()
    rate = models.FloatField()
    discount = models.FloatField(default=0)
    unit = models.ForeignKey(Unit)
    sale = models.ForeignKey(Sale, related_name='rows')

# class InventroyAccount(models.Model):
#     item = models.ForeignKey(Item)
#     dr_amount = models.FloatField(null=True, blank=True)
#     cr_amount = models.FloatField(null=True, blank=True)
#     current_balance = models.FloatField(null=True, blank=True)

# class Transaction(models.Model):
#     date = models.DateField()
#     item = models.ForeignKey(Item)
#     dr_amount = models.FloatField(null=True, blank=True)
#     cr_amount = models.FloatField(null=True, blank=True)








