__author__ = 'xtranophilist'
import django_filters
from bank.models import BankCashDeposit, ChequePayment, ChequeDeposit, ElectronicFundTransferOut, ElectronicFundTransferIn, ElectronicFundTransferInRow
from acubor import filter_extra
from ledger.models import Account


class CashDepositFilter(django_filters.FilterSet):
    date = filter_extra.DateRangeFilter(label='Date Range')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(CashDepositFilter, self).__init__(*args, **kwargs)
        self.filters['bank_account'].field.queryset = Account.objects.filter(company=company, category__name='Bank')
        self.filters['benefactor'].field.queryset = Account.objects.filter(company=company)

    class Meta:
        model = BankCashDeposit
        fields = ['bank_account', 'date', 'benefactor', 'amount']


class ChequeDepositFilter(django_filters.FilterSet):
    date = filter_extra.DateRangeFilter(label='Date Range')
    clearing_date = filter_extra.DateRangeFilter(label='Clearing Date Range')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(ChequeDepositFilter, self).__init__(*args, **kwargs)
        self.filters['bank_account'].field.queryset = Account.objects.filter(company=company, category__name='Bank')
        self.filters['benefactor'].field.queryset = Account.objects.filter(company=company)

    class Meta:
        model = ChequeDeposit
        fields = ['bank_account', 'date', 'clearing_date', 'benefactor']


class ChequePaymentFilter(django_filters.FilterSet):
    cheque_number = django_filters.CharFilter(lookup_type='icontains')
    date = filter_extra.DateRangeFilter(label='Date Range')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(ChequePaymentFilter, self).__init__(*args, **kwargs)
        self.filters['bank_account'].field.queryset = Account.objects.filter(company=company, category__name='Bank')
        self.filters['beneficiary'].field.queryset = Account.objects.filter(company=company)

    class Meta:
        model = ChequePayment
        fields = ['bank_account', 'cheque_number', 'date', 'beneficiary', 'amount']

class ElectronicFundTransferInFilter(django_filters.FilterSet):
    date = filter_extra.DateRangeFilter(label='Date Range')
    clearing_date = filter_extra.DateRangeFilter(label='Clearing Date Range')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(ElectronicFundTransferInFilter, self).__init__(*args, **kwargs)
        self.filters['bank_account'].field.queryset = Account.objects.filter(company=company, category__name='Bank')
        self.filters['benefactor'].field.queryset = Account.objects.filter(company=company)

    class Meta:
        model = ElectronicFundTransferIn
        fields = ['bank_account', 'date', 'clearing_date', 'benefactor']


class ElectronicFundTransferOutFilter(django_filters.FilterSet):
    transaction_number = django_filters.CharFilter(lookup_type='icontains')
    date = filter_extra.DateRangeFilter(label='Date Range')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(ElectronicFundTransferOutFilter, self).__init__(*args, **kwargs)
        self.filters['bank_account'].field.queryset = Account.objects.filter(company=company, category__name='Bank')
        self.filters['beneficiary'].field.queryset = Account.objects.filter(company=company)

    class Meta:
        model = ElectronicFundTransferOut
        fields = ['bank_account', 'transaction_number', 'date', 'beneficiary', 'amount']