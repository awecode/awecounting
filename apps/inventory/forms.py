from django import forms
from modeltranslation.forms import TranslationModelForm
from django.utils.translation import ugettext_lazy as _

from apps.inventory.models import Item, Party, Unit, InventoryAccount
from awecounting.utils.forms import HTML5BootstrapModelForm, KOModelForm


class ItemForm(HTML5BootstrapModelForm, KOModelForm, TranslationModelForm):
    account_no = forms.Field(widget=forms.TextInput(), label=_('Inventory Account No.'))

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)

        if self.instance.account:
            self.fields['account_no'].initial = self.instance.account.account_no
        else:
            self.fields['account_no'].initial = InventoryAccount.get_next_account_no()
        if self.instance.id:
            self.fields['account_no'].widget = forms.HiddenInput()

    def clean_account_no(self):
        if not self.cleaned_data['account_no'].isdigit():
            raise forms.ValidationError("The account no. must be a number.")
        try:
            existing = InventoryAccount.objects.get(account_no=self.cleaned_data['account_no'])
            if self.instance.account.id is not existing.id:
                raise forms.ValidationError("The account no. " + str(
                    self.cleaned_data['account_no']) + " is already in use.")
            return self.cleaned_data['account_no']
        except InventoryAccount.DoesNotExist:
            return self.cleaned_data['account_no']

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['other_properties', 'account', 'unit', 'ledger']


class PartyForm(HTML5BootstrapModelForm):
    address = forms.CharField(label=_('Address'), required=False)
    phone_no = forms.CharField(label=_('Phone No.'), required=False)
    pan_no = forms.CharField(label=_('PAN No.'), required=False)

    class Meta:
        model = Party
        exclude = ('account',)


class UnitForm(HTML5BootstrapModelForm):
    class Meta:
        model = Unit
        fields = '__all__'
