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
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}))
    bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank Account'), empty_label=None,
                                          widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Bank Acc.',
                                                                     'data-url': reverse_lazy(
                                                                         'bank:bankaccount_add')}),
                                                                         # 'create_bank_account')}),
                                                                         # 
                                          label='Beneficiary Account')
    # benefactor = forms.ModelChoiceField(Account.objects.all(), empty_label=None,
    #                                     widget=forms.Select(
    #                                         attrs={'class': 'select2', 'data-url': reverse_lazy('create_account')}))
    benefactor = forms.ModelChoiceField(Account.objects.all(), empty_label=None,
                                        widget=forms.Select(
                                            attrs={'class': 'select2'}))
    attachment = ExtFileField(
        label='Add an attachment',
        help_text='',
        required=False,
        ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
    )

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(BankCashDepositForm, self).__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = Account.objects.filter(company=self.company,
                                                                      category__name='Bank Account')
        self.fields['benefactor'].queryset = Account.objects.filter(company=self.company)

    def clean_voucher_no(self):
        try:
            existing = BankCashDeposit.objects.get(voucher_no=self.cleaned_data['voucher_no'], company=self.company)
            if self.instance.id is not existing.id:
                raise forms.ValidationError("The voucher no. " + str(
                    self.cleaned_data['voucher_no']) + " is already in use.")
            return self.cleaned_data['voucher_no']
        except BankCashDeposit.DoesNotExist:
            return self.cleaned_data['voucher_no']

    class Meta:
        model = BankCashDeposit
        exclude = ['company', 'status']
        

class ChequePaymentForm(HTML5BootstrapModelForm):
    class Meta:
        model = ChequePayment
        exclude = ('company',)
        widgets = {
            'beneficiary': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('account_add')}),
            'bank_account': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('account_add')}),
        }
        company_filters = ('beneficiary', 'bank_account')
