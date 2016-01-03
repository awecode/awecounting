from ..voucher.models import CashReceipt
from awecounting.utils.forms import HTML5BootstrapModelForm, KOModelForm


class CashReceiptForm(HTML5BootstrapModelForm, KOModelForm):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(CashReceiptForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CashReceipt
        exclude = ['company']
