from ..ledger.models import Party
from awecounting.utils.forms import HTML5BootstrapModelForm


class PartyForm(HTML5BootstrapModelForm):
    # def clean(self):
    #     import ipdb
    #     ipdb.set_trace()
    #     pan_no = self.cleaned_data['pan_no']
    #     if pan_no:
    #         conflicting_instance = Party.objects.filter(pan_no=pan_no, company=self.company).exclude(pk=self.pk)
    #         if conflicting_instance.exists():
    #             raise ValidationError(_('Company with this PAN already exists.'))

    class Meta:
        model = Party
        exclude = ('account', 'company')
