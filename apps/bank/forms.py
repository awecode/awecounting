from awecounting.utils.forms import HTML5BootstrapModelForm, ExtFileField, KOModelForm
from .models import BankAccount, BankCashDeposit
from django import forms
from django.core.urlresolvers import reverse_lazy
from apps.ledger.models import Account


class BankAccountForm(HTML5BootstrapModelForm):

    class Meta:
        model = BankAccount
        exclude = ('account', 'company')


class BankCashDepositForm(HTML5BootstrapModelForm, KOModelForm):
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


# from acubor.lib import KOModelForm, ExtFileField
# from models import BankAccount, ChequeDeposit, BankCashDeposit, ChequePayment, ElectronicFundTransferIn, ElectronicFundTransferOut

# class ChequeDepositForm(KOModelForm):
#     bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank Account'), empty_label=None,
#                                           widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Bank Account',
#                                                                      'data-url': reverse_lazy('create_bank_account')}),
#                                           label='Beneficiary Account')
#     benefactor = forms.ModelChoiceField(Account.objects.all(), empty_label=None,
#                                         widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Benefactor',
#                                                                    'data-url': reverse_lazy('create_account')}),
#                                         label='Benefactor (Given By)')
#     date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}))
#     clearing_date = forms.DateField(
#         widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}), required=False)
#     attachment = ExtFileField(
#         label='Add an attachment',
#         help_text='',
#         required=False,
#         ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
#     )

#     def __init__(self, *args, **kwargs):
#         self.company = kwargs.pop('company', None)
#         super(ChequeDepositForm, self).__init__(*args, **kwargs)
#         self.fields['bank_account'].queryset = Account.objects.filter(company=self.company,
#                                                                       category__name='Bank Account')
#         self.fields['benefactor'].queryset = Account.objects.filter(company=self.company)

#     def clean_voucher_no(self):
#         try:
#             existing = ChequeDeposit.objects.get(voucher_no=self.cleaned_data['voucher_no'], company=self.company)
#             if self.instance.id is not existing.id:
#                 raise forms.ValidationError("The voucher no. " + str(
#                     self.cleaned_data['voucher_no']) + " is already in use. Suggested no. has been provided.")
#             return self.cleaned_data['voucher_no']
#         except ChequeDeposit.DoesNotExist:
#             return self.cleaned_data['voucher_no']

#     class Meta:
#         model = ChequeDeposit
#         exclude = ['company', 'status']


# class ElectronicFundTransferInForm(KOModelForm):
#     bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank Account'), empty_label=None,
#                                           widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Bank Account',
#                                                                      'data-url': reverse_lazy('create_bank_account')}),
#                                           label='Beneficiary Account')
#     benefactor = forms.ModelChoiceField(Account.objects.all(), empty_label=None,
#                                         widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Benefactor',
#                                                                    'data-url': reverse_lazy('create_account')}),
#                                         label='Benefactor (Given By)')
#     date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}))
#     clearing_date = forms.DateField(
#         widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}), required=False)
#     attachment = ExtFileField(
#         label='Add an attachment',
#         help_text='',
#         required=False,
#         ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
#     )

#     def clean_voucher_no(self):
#         try:
#             existing = ElectronicFundTransferIn.objects.get(voucher_no=self.cleaned_data['voucher_no'],
#                                                             company=self.company)
#             if self.instance.id is not existing.id:
#                 raise forms.ValidationError("The voucher no. " + str(
#                     self.cleaned_data['voucher_no']) + " is already in use. Suggested no. has been provided.")
#             return self.cleaned_data['voucher_no']
#         except ElectronicFundTransferIn.DoesNotExist:
#             return self.cleaned_data['voucher_no']

#     def __init__(self, *args, **kwargs):
#         self.company = kwargs.pop('company', None)
#         super(ElectronicFundTransferInForm, self).__init__(*args, **kwargs)
#         self.fields['bank_account'].queryset = Account.objects.filter(company=self.company,
#                                                                       category__name='Bank Account')
#         self.fields['benefactor'].queryset = Account.objects.filter(company=self.company)

#     class Meta:
#         model = ElectronicFundTransferIn
#         exclude = ['company', 'status']


# class ChequePaymentForm(KOModelForm):
#     bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank Account'), empty_label=None,
#                                           widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Bank Acc.',
#                                                                      'data-url': reverse_lazy(
#                                                                          'create_bank_account')}))
#     beneficiary = forms.ModelChoiceField(Account.objects.all(), empty_label=None,
#                                          widget=forms.Select(
#                                              attrs={'class': 'select2', 'data-url': reverse_lazy('create_account')}))
#     date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}))
#     attachment = ExtFileField(
#         label='Add an attachment',
#         help_text='',
#         required=False,
#         ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
#     )

#     def __init__(self, *args, **kwargs):
#         company = kwargs.pop('company', None)
#         super(ChequePaymentForm, self).__init__(*args, **kwargs)
#         self.fields['bank_account'].queryset = Account.objects.filter(company=company, category__name='Bank Account')
#         self.fields['beneficiary'].queryset = Account.objects.filter(company=company)

#     class Meta:
#         model = ChequePayment
#         exclude = ['company', 'status']


# class ElectronicFundTransferOutForm(KOModelForm):
#     bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank Account'), empty_label=None,
#                                           widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Bank Acc.',
#                                                                      'data-url': reverse_lazy(
#                                                                          'create_bank_account')}))
#     beneficiary = forms.ModelChoiceField(Account.objects.all(), empty_label=None,
#                                          widget=forms.Select(
#                                              attrs={'class': 'select2', 'data-url': reverse_lazy('create_account')}))
#     date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': "yyyy-mm-dd"}))
#     attachment = ExtFileField(
#         label='Add an attachment',
#         help_text='',
#         required=False,
#         ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
#     )

#     def __init__(self, *args, **kwargs):
#         company = kwargs.pop('company', None)
#         super(ElectronicFundTransferOutForm, self).__init__(*args, **kwargs)
#         self.fields['bank_account'].queryset = Account.objects.filter(company=company, category__name='Bank Account')
#         self.fields['beneficiary'].queryset = Account.objects.filter(company=company)

#     class Meta:
#         model = ElectronicFundTransferOut
#         exclude = ['company', 'status']