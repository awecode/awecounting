import datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.db.models import F
from mptt.models import MPTTModel, TreeForeignKey

from apps.users.models import Company
from awecounting.utils.helpers import zero_for_none, none_for_zero


class Node(object):
    def __init__(self, model, parent=None, depth=0, company=None):
        self.children = []
        self.model = model
        self.name = self.model.name
        self.type = self.model.__class__.__name__
        self.dr = 0
        self.cr = 0
        self.url = None
        self.depth = depth
        self.parent = parent
        self.company = company or str(self.model.company)
        if self.type == 'Category':
            for child in self.model.children.all():
                self.add_child(Node(child, parent=self, depth=self.depth + 1, company=self.company))
            for account in self.model.accounts.all():
                self.add_child(Node(account, parent=self, depth=self.depth + 1, company=self.company))
        if self.type == 'Account':
            self.dr = self.model.current_dr or 0
            self.cr = self.model.current_cr or 0
            self.url = self.model.get_absolute_url()
        if self.parent:
            self.parent.dr += self.dr
            self.parent.cr += self.cr

    def add_child(self, obj):
        self.children.append(obj.get_data())

    def get_data(self):
        data = {
            'name': self.name,
            'type': self.type,
            'dr': round(self.dr, 2),
            'cr': round(self.cr, 2),
            'nodes': self.children,
            'depth': self.depth,
            'url': self.url,
            'company': self.company,
        }
        return data

    def __str__(self):
        return self.name


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=254, null=True, blank=True)
    code = models.CharField(max_length=20, null=True, blank=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.name

    def get_data(self):
        node = Node(self)
        return node.get_data()

    def get_descendant_ledgers(self):
        ledgers = self.accounts.all()
        for descendant in self.get_descendants():
            ledgers = ledgers | descendant.accounts.all()
        return ledgers

    class Meta:
        verbose_name_plural = u'Categories'
        unique_together = ('company', 'name')


class Account(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company)
    current_dr = models.FloatField(null=True, blank=True)
    current_cr = models.FloatField(null=True, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    category = models.ForeignKey(Category, related_name='accounts', blank=True, null=True)
    tax_rate = models.FloatField(blank=True, null=True)
    opening_dr = models.FloatField(default=0)
    opening_cr = models.FloatField(default=0)
    fy = models.PositiveSmallIntegerField(blank=True, null=True)

    _original_opening_dr = 0
    _original_opening_cr = 0

    def __init__(self, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)
        self._original_opening_dr = self.opening_dr
        self._original_opening_cr = self.opening_cr

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

    def suggest_code(self):
        if self.category:
            cat_code = self.category.code or ''
            max = 0
            for account in self.category.accounts.all():
                code = account.code.strip(cat_code + '-')
                if code.isdigit() and int(code) > max:
                    max = int(code)
            if cat_code:
                self.code = cat_code + '-' + str(max + 1)
            else:
                self.code = str(max + 1)

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

    def get_voucher_no(self):
        # Use code as voucher number in ledger view when 
        # an account is the source of journal entry for opening balance transactions
        return self.code

    def save(self, *args, **kwargs):
        if not self.pk:
            queryset = Account.objects.filter(company=self.company)
            original_name = self.name
            nxt = 2
            while queryset.filter(**{'name': self.name}):
                self.name = original_name
                end = '%s%s' % ('-', nxt)
                if len(self.name) + len(end) > 100:
                    self.name = self.name[:100 - len(end)]
                self.name = '%s%s' % (self.name, end)
                nxt += 1
        opening_balance_equity = None
        super(Account, self).save(*args, **kwargs)
        if self.opening_dr != self._original_opening_dr:
            entries = []
            opening_balance_equity = Account.objects.get(name='Opening Balance Equity', category__name='Equity')
            entries.append(['cr', opening_balance_equity, self.opening_dr])
            entries.append(['dr', self, self.opening_dr])
            self._original_opening_dr = self.opening_dr
            set_transactions(self, datetime.date.today(), *entries)
        if self.opening_cr != self._original_opening_cr:
            entries = []
            if not opening_balance_equity:
                opening_balance_equity = Account.objects.get(name='Opening Balance Equity', category__name='Equity')
            entries.append(['dr', opening_balance_equity, self.opening_cr])
            entries.append(['cr', self, self.opening_cr])
            self._original_opening_cr = self.opening_cr
            set_transactions(opening_balance_equity, datetime.date.today(), *entries)

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
    dr_total = 0
    cr_total = 0
    for arg in args:
        # transaction = Transaction(account=arg[1], dr_amount=arg[2])
        matches = journal_entry.transactions.filter(account=arg[1])
        val = round(float(zero_for_none(arg[2])), 2)
        if not matches:
            transaction = Transaction()
            transaction.account = arg[1]
            if arg[0] == 'dr':
                transaction.dr_amount = val
                transaction.cr_amount = None
                transaction.account.current_dr = none_for_zero(zero_for_none(transaction.account.current_dr) + val)
                alter(arg[1], date, val, 0)
                dr_total += val
            if arg[0] == 'cr':
                transaction.cr_amount = val
                transaction.dr_amount = None
                transaction.account.current_cr = none_for_zero(zero_for_none(transaction.account.current_cr) + val)
                alter(arg[1], date, 0, float(arg[2]))
                cr_total += val
            transaction.current_dr = none_for_zero(
                round(zero_for_none(transaction.account.get_dr_amount(date + datetime.timedelta(days=1)))
                      + zero_for_none(transaction.dr_amount), 2)
            )
            transaction.current_cr = none_for_zero(
                round(zero_for_none(transaction.account.get_cr_amount(date + datetime.timedelta(days=1)))
                      + zero_for_none(transaction.cr_amount), 2)
            )
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
                dr_difference = val - zero_for_none(transaction.dr_amount)
                cr_difference = zero_for_none(transaction.cr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.dr_amount = val
                transaction.cr_amount = None
                dr_total += transaction.dr_amount
            else:
                cr_difference = val - zero_for_none(transaction.cr_amount)
                dr_difference = zero_for_none(transaction.dr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.cr_amount = val
                transaction.dr_amount = None
                cr_total += transaction.cr_amount

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
    if dr_total != cr_total:
        mail_admins('Dr/Cr mismatch!',
                    'Dr/Cr mismatch from {0}, ID: {1}, Dr: {2}, Cr: {3}'.format(str(submodel), submodel.id, dr_total, cr_total))
        raise RuntimeError('Dr/Cr mismatch!')


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


# @receiver(pre_delete, sender=Transaction)
def _transaction_delete(sender, instance, **kwargs):
    transaction = instance
    # cancel out existing dr_amount and cr_amount from account's current_dr and current_cr
    if transaction.dr_amount:
        transaction.account.current_dr = zero_for_none(transaction.account.current_dr)
        transaction.account.current_dr -= transaction.dr_amount

    if transaction.cr_amount:
        transaction.account.current_cr = zero_for_none(transaction.account.current_cr)
        transaction.account.current_cr -= transaction.cr_amount

    alter(transaction.account, transaction.journal_entry.date, float(zero_for_none(transaction.dr_amount)) * -1,
          float(zero_for_none(transaction.cr_amount)) * -1)

    transaction.account.save()


pre_delete.connect(_transaction_delete, Transaction, dispatch_uid="apps.ledgers.models")

from apps.users.signals import company_creation


def handle_company_creation(sender, **kwargs):
    company = kwargs.get('company')

    # CREATE DEFAULT CATEGORIES AND LEDGERS FOR EQUITY

    equity = Category.objects.create(name='Equity', code='E', company=company)
    Account.objects.create(name='Paid in Capital', category=equity, code='E-PC', company=company)
    Account.objects.create(name='Retained Earnings', category=equity, code='E-RE', company=company)
    # Account.objects.create(name='Profit and Loss Account', category=equity, code='E-PL', company=company)
    Account.objects.create(name='Opening Balance Equity', category=equity, code='E-OBE', company=company)

    # CREATE DEFAULT CATEGORIES AND LEDGERS FOR ASSETS

    assets = Category.objects.create(name='Assets', code='A', company=company)
    Category.objects.create(name='Other Receivables', code='A-OR', parent=assets, company=company)
    Category.objects.create(name='Tax Receivables', code='A-TR', parent=assets, company=company)
    Category.objects.create(name='Deferred Assets', code='A-DA', parent=assets, company=company)
    Category.objects.create(name='Fixed Assets', code='A-FA', parent=assets, company=company)
    Category.objects.create(name='Loans and Advances Given', code='A-L', parent=assets, company=company)
    Category.objects.create(name='Deposits Made', code='A-D', parent=assets, company=company)
    Category.objects.create(name='Employee', code='A-E', parent=assets, company=company)

    cash_account = Category.objects.create(name='Cash Accounts', code='A-C', parent=assets, company=company)
    Account.objects.create(company=company, name='Cash', category=cash_account, code='A-C-C')
    Account.objects.create(name='Merchandise', category=assets, code='A-M', company=company)
    cash_equivalent_account = Category.objects.create(name='Cash Equivalent Account', code='A-CE', parent=assets, company=company)
    Account.objects.create(name='Cheque Account', category=cash_equivalent_account, code='A-CE-CQ', company=company)

    bank_account = Category.objects.create(name='Bank Account', code='A-B', parent=assets, company=company)
    # Account(name='ATM Account', category=bank_account, code='A-B-A', company=company).save()
    # Account(name='Bank Account', category=bank_account, code='A-B-B', company=company).save()
    # Account(name='Card Account', category=bank_account, code='A-B-Ca', company=company).save()

    account_receivables = Category.objects.create(name='Account Receivables', code='A-AR', parent=assets, company=company)
    Category.objects.create(name='Customers', code='A-AR-C', parent=account_receivables, company=company)

    employee_deductions = Category.objects.create(name='Employee Deductions', code='A-ED', parent=assets, company=company)
    Account.objects.create(name='Advances', category=employee_deductions, code='A-ED-AD', company=company)
    Account.objects.create(name='Loans', category=employee_deductions, code='A-ED-L', company=company)
    Account.objects.create(name='Payroll Taxes', category=employee_deductions, code='A-ED-T', company=company)
    Account.objects.create(name='Employees\' Contribution to Retirement Fund', category=employee_deductions, code='A-ED-RF',
                           company=company)
    Account.objects.create(name='Compulsory Deductions', category=employee_deductions, code='A-ED-CD', company=company)

    # CREATE DEFAULT CATEGORIES AND LEDGERS FOR LIABILITIES

    liabilities = Category.objects.create(name='Liabilities', code='L', company=company)
    account_payables = Category.objects.create(name='Account Payables', code='L-AP', parent=liabilities, company=company)
    Category.objects.create(name='Suppliers', parent=account_payables, code='L-AP-S', company=company)
    other_payables = Category.objects.create(name='Other Payables', code='L-OP', parent=liabilities, company=company)
    Account.objects.create(name='Utility Bills Account', category=other_payables, code='L-OP-U', company=company)
    Category.objects.create(name='Provisions', code='L-P', parent=liabilities, company=company)
    secured_loans = Category.objects.create(name='Secured Loans', code='L-SL', parent=liabilities, company=company)
    Account.objects.create(name='Bank OD', category=secured_loans, code='L-SL-OD', company=company)
    Account.objects.create(name='Bank Loans', category=secured_loans, code='L-SL-BL', company=company)
    Category.objects.create(name='Unsecured Loans', code='L-US', parent=liabilities, company=company)
    Category.objects.create(name='Deposits Taken', code='L-DT', parent=liabilities, company=company)
    Category.objects.create(name='Loans & Advances Taken', code='L-L&A', parent=liabilities, company=company)
    duties_and_taxes = Category.objects.create(name='Duties & Taxes', code='L-T', parent=liabilities, company=company)
    Account.objects.create(name='Sales Tax', category=duties_and_taxes, code='L-T-S', company=company)
    Account.objects.create(name='Payroll Tax', category=duties_and_taxes, code='L-T-P', company=company)
    Account.objects.create(name='Income Tax', category=duties_and_taxes, code='L-T-I', company=company)

    # CREATE DEFAULT CATEGORIES FOR INCOME

    income = Category.objects.create(name='Income', code='I', company=company)
    Category.objects.create(name='Sales', code='I-S', parent=income, company=company)
    direct_income = Category.objects.create(name='Direct Income', code='I-D', parent=income, company=company)
    Category.objects.create(name='Transfer and Remittance', code='I-D-T&R', parent=direct_income, company=company)
    Category.objects.create(name='Indirect Income', code='I-II', parent=income, company=company)

    # CREATE DEFAULT CATEGORIES FOR EXPENSES

    expenses = Category.objects.create(name='Expenses', code='E', company=company)
    Category.objects.create(name='Purchase', code='E-P', parent=expenses, company=company)

    direct_expenses = Category.objects.create(name='Direct Expenses', code='E-DE', parent=expenses, company=company)
    Category.objects.create(name='Purchase Expenses', code='E-DE-PE', parent=direct_expenses, company=company)
    indirect_expenses = Category.objects.create(name='Indirect Expenses', code='E-IE', parent=expenses, company=company)
    Category.objects.create(name='Pay Head', code='E-IE-P', parent=indirect_expenses, company=company)

    # Opening Balance Difference

    # opening_balance_difference = Category.objects.create(name='Opening Balance Difference', code='O', company=company)
    # Account.objects.create(name='Opening Balance Difference', code='O-OBD', category=opening_balance_difference, company=company)

    handle_fy_creation(sender, company=company, fy=company.fy)


def handle_fy_creation(sender, **kwargs):
    company = kwargs.get('company')
    fy = kwargs.get('fy')

    # CREATE DEFAULT LEDGERS FOR INCOME FOR THE FY

    income = Category.objects.get(name='Income', company=company)
    sales = Category.objects.get(name='Sales', parent=income, company=company)
    indirect_income = Category.objects.get(name='Indirect Income', code='I-II', parent=income, company=company)
    Account.objects.create(name='Discount Income', category=indirect_income, code='I-II-DI', company=company, fy=fy)
    Account.objects.create(name='Non-tax Sales', category=sales, code='I-S-NT', company=company, fy=fy)
    Account.objects.create(name='Sales', category=sales, code='I-S-S', company=company, fy=fy)
    direct_income = Category.objects.get(name='Direct Income', parent=income, company=company)
    transfer_remittance = Category.objects.get(name='Transfer and Remittance', parent=direct_income, company=company)
    Account.objects.create(name='Bill Payments', code='I-DI-T&R-BP', category=transfer_remittance, company=company, fy=fy)
    indirect_income = Category.objects.get(name='Indirect Income', parent=income, company=company)
    Account.objects.create(name='Commission In', code='I-II-CI', category=indirect_income, company=company, fy=fy)

    # CREATE DEFAULT LEDGERS FOR EXPENSE FOR THE FY

    expenses = Category.objects.get(name='Expenses', company=company)
    purchase = Category.objects.get(name='Purchase', parent=expenses, company=company)
    Account.objects.create(name='Purchases', code='E-P-P', category=purchase, company=company, fy=fy)

    direct_expenses = Category.objects.get(name='Direct Expenses', parent=expenses, company=company)
    Account.objects.create(name='Wages', category=direct_expenses, code='E-DE-W', company=company, fy=fy)

    indirect_expenses = Category.objects.get(name='Indirect Expenses', parent=expenses, company=company)
    Account.objects.create(name='Payroll Expenses', category=indirect_expenses, code='E-IE-P', company=company, fy=fy)
    Account.objects.create(name='Rent Expenses', category=indirect_expenses, code='E-IE-R', company=company, fy=fy)
    Account.objects.create(name='Commission Out', category=indirect_expenses, code='E-IE-CO', company=company, fy=fy)
    Account.objects.create(name='Bank Charges Expenses', category=indirect_expenses, code='E-IR-BC', company=company, fy=fy)
    Account.objects.create(name='Bank Interest Expenses', category=indirect_expenses, code='E-IE-BI', company=company, fy=fy)
    Account.objects.create(name='Electricity Expenses', category=indirect_expenses, code='E-IE-E', company=company, fy=fy)
    Account.objects.create(name='Telecommunication Expenses', category=indirect_expenses, code='E-IE-T', company=company, fy=fy)

    Account.objects.create(name='Travelling and Conveyance Expenses', category=indirect_expenses, code='E-IE-T&C',
                           company=company, fy=fy)
    Account.objects.create(name='Lunch and Refreshment Expenses', category=indirect_expenses, code='E-IE-L&R',
                           company=company, fy=fy)
    Account.objects.create(name='Cleaning Expenses', category=indirect_expenses, code='E-IE-C', company=company, fy=fy)
    Account.objects.create(name='Discount Expenses', category=indirect_expenses, code='E-IE-D', company=company, fy=fy)
    Account.objects.create(name='Repairs and Maintenance Expenses', category=indirect_expenses, code='E-IE-R&M', company=company,
                           fy=fy)
    Account.objects.create(name='Drainage/Garbage Collection Expenses', category=indirect_expenses, code='E-IE-D&G',
                           company=company, fy=fy)
    Account.objects.create(name='Water Supply Expenses', category=indirect_expenses, code='E-IE-W', company=company, fy=fy)
    Account.objects.create(name='City/Municipal Expenses', category=indirect_expenses, code='E-IE-C&M', company=company, fy=fy)

    purchase_expenses = Category.objects.get(name='Purchase Expenses', parent__name='Direct Expenses', company=company)
    Account.objects.create(name='Carriage Inwards', category=purchase_expenses, code='E-DE-PE-CI', company=company, fy=fy)
    Account.objects.create(name='Customs Duty', category=purchase_expenses, code='E-DE-PE-CD', company=company, fy=fy)

    pay_head = Category.objects.get(name='Pay Head', parent=indirect_expenses, company=company)
    Account.objects.create(name='Salary', category=pay_head, code='E-IE-P-S', company=company, fy=fy)
    Account.objects.create(name='Allowances', category=pay_head, code='E-IE-P-A', company=company, fy=fy)
    Account.objects.create(name='Benefits', category=pay_head, code='E-IE-P-B', company=company, fy=fy)
    Account.objects.create(name='Employees\' Insurance', category=pay_head, code='E-IE-P-I', company=company, fy=fy)
    Account.objects.create(name='Travelling Allowance', category=pay_head, code='E-IE-P-TA', company=company, fy=fy)
    Account.objects.create(name='Daily Allowance', category=pay_head, code='E-IE-P-DA', company=company, fy=fy)


company_creation.connect(handle_company_creation)


class Party(models.Model):
    name = models.CharField(max_length=254)
    address = models.TextField(blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    pan_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='Tax Reg. No.')
    account = models.ForeignKey(Account, null=True)
    TYPES = [('Customer', 'Customer'), ('Supplier', 'Supplier'), ('Customer/Supplier', 'Customer/Supplier')]
    type = models.CharField(choices=TYPES, max_length=17, default='Customer/Supplier')
    supplier_account = models.OneToOneField(Account, null=True, related_name='supplier_detail')
    customer_account = models.OneToOneField(Account, null=True, related_name='customer_detail')
    company = models.ForeignKey(Company, related_name='parties')
    related_company = models.ForeignKey(Company, blank=True, null=True, related_name='related_party')

    def get_absolute_url(self):
        return reverse_lazy('party_edit', kwargs={'pk': self.pk})

    @property
    def balance(self):
        return zero_for_none(self.customer_account.current_dr) - zero_for_none(
            self.customer_account.current_cr) + zero_for_none(
            self.supplier_account.current_cr) - zero_for_none(self.supplier_account.current_dr)

    def save(self, *args, **kwargs):
        self.post = kwargs.pop('post', True)
        super(Party, self).save(*args, **kwargs)

        if self.post:
            self.post_save()

    def post_save(self):
        account = Account(name=self.name)
        account.company = self.company
        if self.type == 'Customer':
            if not self.customer_account:
                try:
                    account.category = Category.objects.get(name='Customers', company=self.company)
                    account.suggest_code()
                    account.save()
                    self.customer_account = account
                except Category.DoesNotExist:
                    pass
            if self.supplier_account:
                self.supplier_account.delete()
                self.supplier_account = None
        elif self.type == 'Supplier':
            if not self.supplier_account:
                try:
                    account.category = Category.objects.get(name='Suppliers', company=self.company)
                    account.suggest_code()
                    account.save()
                    self.supplier_account = account
                except Category.DoesNotExist:
                    pass
            if self.customer_account:
                self.customer_account.delete()
                self.customer_account = None
        else:
            if not self.customer_account:
                account.name += ' (Receivable)'
                try:
                    account.category = Category.objects.get(name='Customers', company=self.company)
                    account.suggest_code()
                    account.save()
                    self.customer_account = account
                except Category.DoesNotExist:
                    pass
            if not self.supplier_account:
                try:
                    account2 = Account(name=self.name + ' (Payable)')
                    account2.company = self.company
                    account2.category = Category.objects.get(name='Suppliers', company=self.company)
                    account2.suggest_code()
                    account2.save()
                    self.supplier_account = account2
                except Category.DoesNotExist:
                    pass
        self.save(post=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Parties'
        unique_together = ('company', 'related_company')

        # @receiver(branch_creation)
        # def handle_branch_creation(sender, **kwargs):
        # Party.objects.create(name=kwargs['name'], company=kwargs['company'])
        # print "Handle branch"
        # pass


def get_account(request_or_company, name):
    if not request_or_company.__class__.__name__ == 'Company':
        company = request_or_company.company
    else:
        company = request_or_company
    if name in ['Purchase', 'Purchases']:
        return Account.objects.get(name='Purchase', category__name='Purchase', company=company)
    if name in ['Cash', 'Cash Account']:
        return Account.objects.get(name='Cash', category__name='Cash Accounts', company=company)
