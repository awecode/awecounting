from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from ..ledger.models import Party, Account, Category
from awecounting.utils.forms import HTML5BootstrapModelForm


class PartyForm(HTML5BootstrapModelForm):
    def clean_pan_no(self):
        pan_no = self.cleaned_data['pan_no']
        if pan_no:
            conflicting_instance = Party.objects.filter(pan_no=pan_no, company=self.company).exclude(
                pk=self.instance.pk)
            if conflicting_instance.exists():
                raise ValidationError(_('Company with this PAN already exists.'))
        return pan_no

    class Meta:
        model = Party
        exclude = ('account', 'company', 'related_company', 'customer_account', 'supplier_account')


class AccountForm(HTML5BootstrapModelForm):
    class Meta:
        model = Account
        exclude = ('parent', 'company', 'tax_rate')


class CategoryForm(HTML5BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CategoryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Category
        exclude = ('company', 'default')
        widgets = {
            'parent': forms.Select(attrs={'class': 'selectize'}),
        }
        company_filters = ('parent',)

    def clean(self):
        data = super(CategoryForm, self).clean()
        try:
            Category.objects.get(name=data['name'], company=self.request.company)
        except Category.DoesNotExist:
            pass
        else:
            raise ValidationError('Category Name already exists.')
        return data
