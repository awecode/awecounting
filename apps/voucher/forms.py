from ..ledger.models import Account
from ..voucher.models import CreditVoucher, DebitVoucher
from awecounting.utils.forms import HTML5BootstrapModelForm, KOModelForm
from .models import JournalVoucher, VoucherSetting
from django import forms
from django.core.urlresolvers import reverse_lazy


class CreditVoucherForm(HTML5BootstrapModelForm, KOModelForm):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(CreditVoucherForm, self).__init__(*args, **kwargs)
        queryset = Account.objects.filter(company=self.company)
        categories = ['Cash Equivalent Account', 'Cash Accounts', 'Bank Account']
        queryset = queryset.filter(category__name__in=categories)
        self.fields['receipt'].queryset = queryset

    class Meta:
        model = CreditVoucher
        exclude = ['company']
        widgets = {
            'receipt': forms.Select(attrs={'class': 'selectize'}),
        }
        company_filters = ('receipt',)

class DebitVoucherForm(HTML5BootstrapModelForm, KOModelForm):

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(DebitVoucherForm, self).__init__(*args, **kwargs)
        queryset = Account.objects.filter(company=self.company)
        categories = ['Cash Equivalent Account', 'Cash Accounts', 'Bank Account']
        queryset = queryset.filter(category__name__in=categories)
        self.fields['payment'].queryset = queryset

    class Meta:
        model = DebitVoucher
        exclude = ['company']
        widgets = {
            'payment': forms.Select(attrs={'class': 'selectize'}),
        }
        company_filters = ('payment',)


class JournalVoucherForm(HTML5BootstrapModelForm):
    class Meta:
        model = JournalVoucher
        fields = '__all__'


class VoucherSettingForm(HTML5BootstrapModelForm):
    class Meta:
        model = VoucherSetting
        exclude = ('company', 'voucher_number_start_date')
        widgets = {
            'sale_default_tax_application_type': forms.Select(attrs={'class': 'selectize'}),
            'purchase_default_tax_application_type': forms.Select(attrs={'class': 'selectize'}),
            'sale_default_tax_scheme': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('tax_scheme_add')}),
            'purchase_default_tax_scheme': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('tax_scheme_add')}),
        }
        company_filters = ('sale_default_tax_scheme', 'purchase_default_tax_scheme')

