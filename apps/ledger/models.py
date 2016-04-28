import datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from django.db.models import F

from apps.users.models import Company
from awecounting.utils.helpers import zero_for_none, none_for_zero


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=254, null=True, blank=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Categories'


class Account(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company)
    current_dr = models.FloatField(null=True, blank=True)
    current_cr = models.FloatField(null=True, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    category = models.ForeignKey(Category, related_name='accounts', blank=True, null=True)
    tax_rate = models.FloatField(blank=True, null=True)
    opening_dr = models.FloatField(default=0)
    opening_cr = models.FloatField(default=0)

    def get_absolute_url(self):
        # return '/ledger/' + str(self.id)
        return reverse('view_ledger', kwargs={'pk': self.pk})

    # def get_last_day_last_transaction(self):
    #     transactions = Transaction.objects.filter(account=self, date__lt=date.today()).order_by('-id', '-date')[:1]
    #     if len(transactions) > 0:
    #         return transactions[0]
    #
    # def get_last_transaction_before(self, before_date):
    #     transactions = Transaction.objects.filter(account=self, date__lt=before_date).order_by('-id', '-date')[:1]
    #     if len(transactions) > 0:
    #         return transactions[0]
    #
    @property
    def balance(self):
        return self.get_balance()

    def get_balance(self):
        return zero_for_none(self.current_dr) - zero_for_none(self.current_cr)

    def get_day_opening_dr(self, before_date=None):
        if not before_date:
            before_date = datetime.date.today()
        transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_dr
        return self.current_dr

    def get_day_opening_cr(self, before_date=None):
        if not before_date:
            before_date = datetime.date.today()
        transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_cr
        return self.current_cr

    def get_day_opening(self, before_date=None):
        if not before_date:
            before_date = datetime.date.today()
        transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return zero_for_none(transactions[0].current_dr) - zero_for_none(transactions[0].current_cr)
        return self.opening_dr - self.opening_cr

    # day_opening_dr = property(get_day_opening_dr)
    # day_opening_cr = property(get_day_opening_cr)
    #
    # day_opening = property(get_day_opening)

    def add_category(self, category):
        # all_categories = self.get_all_categories()
        category_instance, created = Category.objects.get_or_create(name=category, company=self.company)
        # self.categories.add(category_instance)
        self.category = category_instance

    def get_all_categories(self):
        return self.category.get_ancestors(include_self=True)

    categories = property(get_all_categories)

    def get_cr_amount(self, day):
        # journal_entry= JournalEntry.objects.filter(date__lt=day,transactions__account=self).order_by('-id','-date')[:1]
        transactions = Transaction.objects.filter(journal_entry__date__lt=day, account=self).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_cr
        return 0

    def get_dr_amount(self, day):
        # journal_entry= JournalEntry.objects.filter(date__lt=day,transactions__account=self).order_by('-id','-date')[:1]
        transactions = Transaction.objects.filter(journal_entry__date__lt=day, account=self).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_dr
        return 0

    def save(self, *args, **kwargs):
        queryset = Account.objects.filter(company=self.company)
        original_name = self.name
        nxt = 2
        if not self.pk:
            while queryset.filter(**{'name': self.name}):
                self.name = original_name
                end = '%s%s' % ('-', nxt)
                if len(self.name) + len(end) > 100:
                    self.name = self.name[:100 - len(end)]
                self.name = '%s%s' % (self.name, end)
                nxt += 1
        return super(Account, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'company')


class JournalEntry(models.Model):
    date = models.DateField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    source = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.content_type) + ': ' + str(self.object_id) + ' [' + str(self.date) + ']'

    class Meta:
        verbose_name_plural = u'Journal Entries'


class Transaction(models.Model):
    account = models.ForeignKey(Account)
    dr_amount = models.FloatField(null=True, blank=True)
    cr_amount = models.FloatField(null=True, blank=True)
    current_dr = models.FloatField(null=True, blank=True)
    current_cr = models.FloatField(null=True, blank=True)
    journal_entry = models.ForeignKey(JournalEntry, related_name='transactions')

    def get_balance(self):
        return zero_for_none(self.current_dr) - zero_for_none(self.current_cr)

    def __str__(self):
        return str(self.account) + ' [' + str(self.dr_amount) + ' / ' + str(self.cr_amount) + ']'


def alter(account, date, dr_difference, cr_difference):
    Transaction.objects.filter(journal_entry__date__gt=date, account=account).update(
        current_dr=none_for_zero(zero_for_none(F('current_dr')) + zero_for_none(dr_difference)),
        current_cr=none_for_zero(zero_for_none(F('current_cr')) + zero_for_none(cr_difference)))


def set_transactions(submodel, date, *args):
    if isinstance(date, unicode):
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    journal_entry, created = JournalEntry.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(submodel), object_id=submodel.id,
        defaults={
            'date': date
        })
    for arg in args:
        # transaction = Transaction(account=arg[1], dr_amount=arg[2])
        matches = journal_entry.transactions.filter(account=arg[1])
        if not matches:
            transaction = Transaction()
            transaction.account = arg[1]
            if arg[0] == 'dr':
                transaction.dr_amount = float(zero_for_none(arg[2]))
                transaction.cr_amount = None
                transaction.account.current_dr = none_for_zero(
                    zero_for_none(transaction.account.current_dr) + transaction.dr_amount)
                alter(arg[1], date, float(arg[2]), 0)
            if arg[0] == 'cr':
                transaction.cr_amount = float(zero_for_none(arg[2]))
                transaction.dr_amount = None
                transaction.account.current_cr = none_for_zero(
                    zero_for_none(transaction.account.current_cr) + transaction.cr_amount)
                alter(arg[1], date, 0, float(arg[2]))
            transaction.current_dr = none_for_zero(
                zero_for_none(transaction.account.get_dr_amount(date + datetime.timedelta(days=1)))
                + zero_for_none(transaction.dr_amount))
            transaction.current_cr = none_for_zero(
                zero_for_none(transaction.account.get_cr_amount(date + datetime.timedelta(days=1)))
                + zero_for_none(transaction.cr_amount))
        else:
            transaction = matches[0]
            transaction.account = arg[1]

            # cancel out existing dr_amount and cr_amount from current_dr and current_cr
            # if transaction.dr_amount:
            #     transaction.current_dr -= transaction.dr_amount
            #     transaction.account.current_dr -= transaction.dr_amount
            #
            # if transaction.cr_amount:
            #     transaction.current_cr -= transaction.cr_amount
            #     transaction.account.current_cr -= transaction.cr_amount

            # save new dr_amount and add it to current_dr/cr
            if arg[0] == 'dr':
                dr_difference = float(arg[2]) - zero_for_none(transaction.dr_amount)
                cr_difference = zero_for_none(transaction.cr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.dr_amount = float(arg[2])
                transaction.cr_amount = None
            else:
                cr_difference = float(arg[2]) - zero_for_none(transaction.cr_amount)
                dr_difference = zero_for_none(transaction.dr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.cr_amount = float(arg[2])
                transaction.dr_amount = None

            transaction.current_dr = none_for_zero(zero_for_none(transaction.current_dr) + dr_difference)
            transaction.current_cr = none_for_zero(zero_for_none(transaction.current_cr) + cr_difference)
            transaction.account.current_dr = none_for_zero(
                zero_for_none(transaction.account.current_dr) + dr_difference)
            transaction.account.current_cr = none_for_zero(
                zero_for_none(transaction.account.current_cr) + cr_difference)

        # the following code lies outside if,else block, inside for loop
        transaction.account.save()
        try:
            journal_entry.transactions.add(transaction, bulk=False)
        except TypeError:  # for Django <1.9
            journal_entry.transactions.add(transaction)


def delete_rows(rows, model):
    for row in rows:
        if row.get('id'):
            instance = model.objects.get(id=row.get('id'))
            try:
                JournalEntry.objects.get(content_type=ContentType.objects.get_for_model(model),
                                         model_id=instance.id).delete()
            except:
                pass
            instance.delete()


@receiver(pre_delete, sender=Transaction)
def _transaction_delete(sender, instance, **kwargs):
    transaction = instance
    # cancel out existing dr_amount and cr_amount from account's current_dr and current_cr
    if transaction.dr_amount:
        transaction.account.current_dr -= transaction.dr_amount

    if transaction.cr_amount:
        transaction.account.current_cr -= transaction.cr_amount

    alter(transaction.account, transaction.journal_entry.date, float(zero_for_none(transaction.dr_amount)) * -1,
          float(zero_for_none(transaction.cr_amount)) * -1)

    transaction.account.save()


from apps.users.signals import company_creation


def handle_company_creation(sender, **kwargs):
    company = kwargs.get('company')

    # EQUITY

    equity = Category(name='Equity', company=company)
    equity.save()
    Account(name='Paid in Capital', category=equity, code='1-0001', company=company).save()
    Account(name='Retained Earnings', category=equity, code='1-0002', company=company).save()
    Account(name='Profit and Loss Account', category=equity, code='1-0003', company=company).save()

    # ASSETS

    assets = Category(name='Assets', company=company)
    assets.save()
    Category(name='Other Receivables', parent=assets, company=company).save()
    Category(name='Deferred Assets', parent=assets, company=company).save()
    Category(name='Fixed Assets', parent=assets, company=company).save()
    Category(name='Loads and Advances Given', parent=assets, company=company).save()
    Category(name='Deposits Made', parent=assets, company=company).save()
    Category(name='Employee', parent=assets, company=company).save()

    cash_account = Category(name='Cash Account', parent=assets, company=company)
    cash_account.save()
    Account.objects.create(company=company, name='Cash', category=cash_account, code='2-0001')

    Account(name='Merchandise', category=assets, code='2-0002', company=company).save()

    cash_equivalent_account = Category(name='Cash Equivalent Account', parent=assets, company=company)
    cash_equivalent_account.save()
    Account(name='Cheque Account', category=cash_equivalent_account, code='2-0003', company=company).save()

    bank_account = Category(name='Bank Account', parent=assets, company=company)
    bank_account.save()
    # Account(name='ATM Account', category=bank_account, code='2-0005', company=company).save()
    # Account(name='Bank Account', category=bank_account, code='2-0001', company=company).save()
    # Account(name='Card Account', category=bank_account, code='2-0002', company=company).save()

    account_receivables = Category(name='Account Receivables', parent=assets, company=company)
    account_receivables.save()
    Category(name='Customers', parent=account_receivables, company=company).save()

    employee_deductions = Category(name='Employee Deductions', parent=assets, company=company)
    employee_deductions.save()
    Account(name='Advances', category=employee_deductions, code='2-0010', company=company).save()
    Account(name='Loans', category=employee_deductions, code='2-0011', company=company).save()
    Account(name='Payroll Taxes', category=employee_deductions, code='2-0012', company=company).save()
    Account(name='Employees\' Contribution to Retirement Fund', category=employee_deductions, code='2-0013',
            company=company).save()
    Account(name='Compulsory Deductions', category=employee_deductions, code='2-0014', company=company).save()

    # LIABILITIES

    liabilities = Category(name='Liabilities', company=company)
    liabilities.save()
    account_payables = Category(name='Account Payables', parent=liabilities, company=company)
    account_payables.save()
    Category(name='Suppliers', parent=account_payables, company=company).save()
    other_payables = Category(name='Other Payables', parent=liabilities, company=company)
    other_payables.save()
    Account(name='Utility Bills Account', category=other_payables, code='3-0002', company=company).save()
    Category(name='Provisions', parent=liabilities, company=company).save()
    secured_loans = Category(name='Secured Loans', parent=liabilities, company=company)
    secured_loans.save()
    Account(name='Bank OD', category=secured_loans, code='3-0005', company=company).save()
    Account(name='Bank Loans', category=secured_loans, code='3-0006', company=company).save()
    Category(name='Unsecured Loans', parent=liabilities, company=company).save()
    Category(name='Deposits Taken', parent=liabilities, company=company).save()
    Category(name='Loans & Advances Taken', parent=liabilities, company=company).save()
    duties_and_taxes = Category(name='Duties & Taxes', parent=liabilities, company=company)
    duties_and_taxes.save()
    Account(name='Sales Tax', category=duties_and_taxes, code='3-0010', company=company).save()
    Account(name='Payroll Tax', category=duties_and_taxes, code='3-0011', company=company).save()
    Account(name='Income Tax', category=duties_and_taxes, code='3-0012', company=company).save()
    # Account(name='VAT', category=duties_and_taxes, code='3-0020', company=company).save()

    # INCOME

    income = Category(name='Income', company=company)
    income.save()
    Account(name='Discount Income', category=income, code='4-0012', company=company).save()
    sales = Category(name='Sales', parent=income, company=company)
    sales.save()

    Account(name='Non Tax Sales', category=sales, code='4-0006', company=company).save()
    Account(name='Sales', category=sales, tax_rate=8.25, code='4-0008', company=company).save()

    direct_income = Category(name='Direct Income', parent=income, company=company)
    direct_income.save()
    transfer_remittance = Category(name='Transfer and Remittance', parent=direct_income, company=company)
    transfer_remittance.save()
    Account(name='Bill Payments', category=transfer_remittance, code='4-0011', company=company).save()

    indirect_income = Category(name='Indirect Income', parent=income, company=company)
    indirect_income.save()
    Account(name='Commission In', category=indirect_income, code='6-0001', company=company).save()

    # EXPENSES

    expenses = Category(name='Expenses', company=company)
    expenses.save()
    purchase = Category(name='Purchase', parent=expenses, company=company)
    purchase.save()
    Account(name='Purchase', category=purchase, code='11-0008', company=company).save()

    Category(name='Direct Expenses', parent=expenses, company=company).save()

    indirect_expenses = Category(name='Indirect Expenses', parent=expenses, company=company)
    indirect_expenses.save()
    Account(name='Payroll Expenses', category=indirect_expenses, code='13-0001', company=company).save()
    Account(name='Rent Expenses', category=indirect_expenses, code='13-0002', company=company).save()
    Account(name='Commission Out', category=indirect_expenses, code='13-0003', company=company).save()
    Account(name='Bank Charges Expenses', category=indirect_expenses, code='13-0004', company=company).save()
    Account(name='Bank Interest Expenses', category=indirect_expenses, code='13-0005', company=company).save()
    Account(name='Electricity Expenses', category=indirect_expenses, code='13-0006', company=company).save()
    Account(name='City/Municipal Expenses', category=indirect_expenses, code='13-0007', company=company).save()
    Account(name='Travelling and Conveyance Expenses', category=indirect_expenses, code='13-0008',
            company=company).save()
    Account(name='Lunch and Refreshment Expenses', category=indirect_expenses, code='13-0009', company=company).save()
    Account(name='Cleaning Expenses', category=indirect_expenses, code='13-0010', company=company).save()
    Account(name='Discount Expenses', category=indirect_expenses, code='13-0011', company=company).save()
    Account(name='Repairs and Maintenance Expenses', category=indirect_expenses, code='13-0012', company=company).save()

    pay_head = Category(name='Pay Head', parent=indirect_expenses, company=company)
    pay_head.save()
    Account(name='Salary', category=pay_head, code='13-0013', company=company).save()
    Account(name='Allowances', category=pay_head, code='13-0014', company=company).save()
    Account(name='Benefits', category=pay_head, code='13-0015', company=company).save()
    Account(name='Employees\' Insurance', category=pay_head, code='13-0016', company=company).save()
    Account(name='Travelling Allowance', category=pay_head, code='13-0017', company=company).save()
    Account(name='Daily Allowance', category=pay_head, code='13-0018', company=company).save()

    # Opening Balance Difference

    opening_balance_difference = Category(name='Opening Balance Difference', company=company)
    opening_balance_difference.save()
    Account(name='Opening Balance Difference', category=opening_balance_difference, company=company,
            code='0-0001').save()


company_creation.connect(handle_company_creation)


class Party(models.Model):
    name = models.CharField(max_length=254)
    address = models.TextField(blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    pan_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='Tax Reg. No.')
    account = models.ForeignKey(Account, null=True)
    TYPES = [('Customer', 'Customer'), ('Supplier', 'Supplier'), ('Customer/Supplier', 'Customer/Supplier')]
    type = models.CharField(choices=TYPES, max_length=17, default='Customer/Supplier')
    supplier_ledger = models.OneToOneField(Account, null=True, related_name='supplier_detail')
    customer_ledger = models.OneToOneField(Account, null=True, related_name='customer_detail')
    company = models.ForeignKey(Company, related_name='parties')
    related_company = models.OneToOneField(Company, blank=True, null=True, related_name='related_party')

    def get_absolute_url(self):
        return reverse_lazy('party_edit', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Party, self).save(*args, **kwargs)
        ledger = Account(name=self.name)
        ledger.company = self.company
        if self.type == 'Customer':
            if not self.customer_ledger:
                ledger.category = Category.objects.get(name='Customers', company=self.company)
                ledger.code = 'C-' + str(self.id)
                ledger.save()
                self.customer_ledger = ledger
            if self.supplier_ledger:
                self.supplier_ledger.delete()
                self.supplier_ledger = None
        elif self.type == 'Supplier':
            if not self.supplier_ledger:
                ledger.category = Category.objects.get(name='Suppliers', company=self.company)
                ledger.code = 'S-' + str(self.id)
                ledger.save()
                self.supplier_ledger = ledger
            if self.customer_ledger:
                self.customer_ledger.delete()
                self.customer_ledger = None
        else:
            if not self.customer_ledger:
                ledger.name += ' (Receivable)'
                ledger.category = Category.objects.get(name='Customers', company=self.company)
                ledger.code = 'C-' + str(self.id)
                ledger.save()
                self.customer_ledger= ledger
            if not self.supplier_ledger:
                ledger2 = Account(name=self.name + ' (Payable)')
                ledger2.company = self.company
                ledger2.category = Category.objects.get(name='Suppliers', company=self.company)
                ledger2.code = 'S-' + str(self.id)
                ledger2.save()
                self.supplier_ledger = ledger2
        super(Party, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Parties'
        unique_together = ['company', 'related_company']


def get_ledger(company, name):
    if not company.__class__.__name__ == 'Company':
        company = company.company
    if name in ['Purchase', 'Purchases']:
        return Account.objects.get(name='Purchase', category__name='Purchase', company=company)
    if name in ['Cash', 'Cash Account']:
        return Account.objects.get(name='Cash', category__name='Cash Account', company=company)
