from django import forms
from awecounting.utils.forms import HTML5BootstrapModelForm, KOModelForm

class ImportDebtor(forms.Form):
    file = forms.FileField()
    new_party = forms.BooleanField(required=False)