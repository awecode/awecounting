from ..voucher.models import CashReceipt, CashPayment
from awecounting.utils.forms import HTML5BootstrapModelForm, KOModelForm
from .models import JournalVoucher, VoucherSetting, Location
from django import forms
from django.core.urlresolvers import reverse_lazy


class CashReceiptForm(HTML5BootstrapModelForm, KOModelForm):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(CashReceiptForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CashReceipt
        exclude = ['company']


class CashPaymentForm(HTML5BootstrapModelForm, KOModelForm):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(CashPaymentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CashPayment
        exclude = ['company']


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

class LocationForm(HTML5BootstrapModelForm):
    class Meta:
        model = Location
        fields = '__all__'