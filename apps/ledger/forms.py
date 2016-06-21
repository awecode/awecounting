from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from ..ledger.models import Party, Account, Category
from awecounting.utils.forms import HTML5BootstrapModelForm


class PartyForm(HTML5BootstrapModelForm):
    # TODO Implement unique pan number by party
    # def clean(self):
    #     pan_no = self.cleaned_data['pan_no']
    #     if pan_no:
    #         conflicting_instance = Party.objects.filter(pan_no=pan_no, company=self.instance.company).exclude(pk=self.instance.pk)
    #         if conflicting_instance.exists():
    #             raise ValidationError(_('Company with this PAN already exists.'))
    #     return pan_no

    class Meta:
        model = Party
        exclude = ('account', 'company', 'related_company', 'customer_account', 'supplier_account')


class AccountForm(HTML5BootstrapModelForm):
    class Meta:
        model = Account
        exclude = ('parent', 'company', 'tax_rate')


class CategoryForm(HTML5BootstrapModelForm):
    class Meta:
        model = Category
        exclude = ('parent', 'company')
