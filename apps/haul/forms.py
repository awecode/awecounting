from django import forms
from awecounting.utils.forms import HTML5BootstrapModelForm, KOModelForm

class ImportFile(forms.Form):
    file = forms.FileField(required=True)
    new_party = forms.BooleanField(required=False)