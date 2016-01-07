from django.core.exceptions import ValidationError
from ..ledger.models import Party
from awecounting.utils.forms import HTML5BootstrapModelForm
from django.utils.translation import ugettext_lazy as _


class PartyForm(HTML5BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('request').company
        return super(PartyForm, self).__init__(*args, **kwargs)

    def clean_pan_no(self):
        pan_no = self.cleaned_data['pan_no']
        if pan_no:
            conflicting_instance = Party.objects.filter(pan_no=pan_no, company=self.company).exclude(pk=self.instance.pk)
            if conflicting_instance.exists():
                raise ValidationError(_('Company with this PAN already exists.'))
        return pan_no

    class Meta:
        model = Party
        exclude = ('account', 'company')
