from awecounting.utils.forms import HTML5BootstrapModelForm, ExtFileField, KOModelForm
from .models import BankAccount, BankCashDeposit, ChequePayment
from django import forms
from django.core.urlresolvers import reverse_lazy
from apps.ledger.models import Account


class BankAccountForm(HTML5BootstrapModelForm):

    class Meta:
        model = BankAccount
        exclude = ('account', 'company')

class BankCashDepositForm(HTML5BootstrapModelForm):
    class Meta:
        model = BankCashDeposit
        exclude = ('company',)
        widgets = {
            'benefactor': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('account_add')}),
            'bank_account': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('account_add')}),
        }
        company_filters = ('benefactor', 'bank_account')


class ChequePaymentForm(HTML5BootstrapModelForm):
    class Meta:
        model = ChequePayment
        exclude = ('company',)
        widgets = {
            'beneficiary': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('account_add')}),
            'bank_account': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('account_add')}),
        }
        company_filters = ('beneficiary', 'bank_account')
