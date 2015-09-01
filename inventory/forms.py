from django import forms
from modeltranslation.forms import TranslationModelForm
from inventory.models import Item, Party, Unit
from django.utils.translation import ugettext_lazy as _


class KOModelForm(forms.ModelForm):
    class EmailTypeInput(forms.widgets.TextInput):
        input_type = 'email'

    class NumberTypeInput(forms.widgets.TextInput):
        input_type = 'number'

    class TelephoneTypeInput(forms.widgets.TextInput):
        input_type = 'tel'

    class DateTypeInput(forms.widgets.DateInput):
        input_type = 'date'

    class DateTimeTypeInput(forms.widgets.DateTimeInput):
        input_type = 'datetime'

    class TimeTypeInput(forms.widgets.TimeInput):
        input_type = 'time'

    def __init__(self, *args, **kwargs):
        super(KOModelForm, self).__init__(*args, **kwargs)
        self.refine()

    def refine(self):
        for (name, field) in self.fields.items():
            # add HTML5 required attribute for required fields
            if field.required:
                field.widget.attrs['required'] = 'required'
            field.widget.attrs['data-bind'] = 'value: ' + name
            field.widget.attrs['class'] = 'form-control'

class ItemForm(KOModelForm, TranslationModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['other_properties']

class PartyForm(KOModelForm):
    address = forms.CharField(label=_('Address'), required=False)
    phone_no = forms.CharField(label=_('Phone No.'), required=False)
    pan_no = forms.CharField(label=_('PAN No.'), required=False)

    class Meta:
        model = Party
        fields = '__all__'

class UnitForm(KOModelForm):
    class Meta:
        model = Unit
        fields = '__all__'
