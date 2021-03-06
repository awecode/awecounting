from django import forms
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from modeltranslation.forms import TranslationModelForm
from .models import Item, Unit, InventoryAccount, UnitConversion, Location, ItemCategory
from awecounting.utils.forms import HTML5BootstrapModelForm, KOModelForm


class ItemForm(HTML5BootstrapModelForm, KOModelForm, TranslationModelForm):
    account_no = forms.Field(widget=forms.TextInput(), label=_('Inventory Account No.'), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ItemForm, self).__init__(*args, **kwargs)
        if self.instance.company_id:
            self.company = self.instance.company
        else:
            self.company = self.request.company

        if self.instance.account:
            self.fields['account_no'].initial = self.instance.account.account_no
        else:
            self.fields['account_no'].initial = InventoryAccount.get_next_account_no(company=self.company)
        if self.instance.id:
            self.fields['account_no'].widget = forms.HiddenInput()
        self.fields['unit'].queryset = Unit.objects.filter(company=self.company)
        self.fields['category'].queryset = ItemCategory.objects.filter(company=self.company)

    def clean_account_no(self):
        if not self.cleaned_data['account_no'].isdigit():
            raise forms.ValidationError("The account no. must be a number.")
        try:
            existing = InventoryAccount.objects.get(account_no=self.cleaned_data['account_no'], company=self.company)
            if not self.instance.id:
                if self.instance.account_id is not existing.id:
                    raise forms.ValidationError("The account no. " + str(
                        self.cleaned_data['account_no']) + " is already in use.")
            return self.cleaned_data['account_no']
        except InventoryAccount.DoesNotExist:
            return self.cleaned_data['account_no']

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['other_properties', 'account', 'ledger', 'company', 'sale_ledger', 'purchase_ledger']
        widgets = {
            'unit': forms.Select(attrs={'data-url': reverse_lazy('unit_add'), 'class': 'selectize'}),
            'category': forms.Select(attrs={'data-url': reverse_lazy('item_category_add'), 'class': 'selectize'}),
        }
        company_filters = ['unit', 'category']


class UnitForm(HTML5BootstrapModelForm):
    class Meta:
        model = Unit
        exclude = ('company',)


class UnitConversionForm(HTML5BootstrapModelForm):
    class Meta:
        model = UnitConversion
        exclude = ('company',)
        widgets = {
            'base_unit': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('unit_add')}),
            'unit_to_convert': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('unit_add')}),
        }
        company_filters = ('base_unit', 'unit_to_convert')


class LocationForm(HTML5BootstrapModelForm):
    class Meta:
        model = Location
        exclude = ('company',)


class ItemCategoryForm(HTML5BootstrapModelForm):
    class Meta:
        model = ItemCategory
        exclude = ('company',)
        widgets = {
            'parent': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('item_category_add')}),
        }
