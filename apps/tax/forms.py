from awecounting.utils.forms import HTML5BootstrapModelForm
from django import forms
from .models import TaxScheme


class TaxSchemeForm(HTML5BootstrapModelForm):
    class Meta:
        model = TaxScheme
        exclude = ('company', 'ledger')
