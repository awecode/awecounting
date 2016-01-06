from ..voucher.models import CashReceipt, CashPayment
from awecounting.utils.forms import HTML5BootstrapModelForm, KOModelForm
from .models import JournalVoucher


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
