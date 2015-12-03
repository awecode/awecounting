from django.core.urlresolvers import reverse_lazy
from awecounting.utils.forms import HTML5BootstrapModelForm
from django import forms
from .models import ShareHolder, Collection, Investment


class ShareHolderForm(HTML5BootstrapModelForm):
    class Meta:
        model = ShareHolder
        exclude = ('company',)


class CollectionForm(HTML5BootstrapModelForm):
    class Meta:
        model = Collection
        exclude = ('company',)


class InvestmentForm(HTML5BootstrapModelForm):
    # share_holder = forms.ModelChoiceField(queryset=ShareHolder.objects.filter(company=self.company))
    class Meta:
        model = Investment
        exclude = ()
        widgets = {
            'share_holder': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('share:shareholder_add')}),
        }
