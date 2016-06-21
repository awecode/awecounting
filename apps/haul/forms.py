from django import forms


class ImportFile(forms.Form):
    file = forms.FileField(required=True)
    new_party = forms.BooleanField(required=False)
