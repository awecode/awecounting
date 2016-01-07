from django.core.urlresolvers import reverse_lazy
from awecounting.utils.forms import HTML5BootstrapModelForm
from django import forms
from .models import ShareHolder, Collection, Investment


class ShareHolderForm(HTML5BootstrapModelForm):
    class Meta:
        model = ShareHolder
        exclude = ('company', 'account')


class CollectionForm(HTML5BootstrapModelForm):
    class Meta:
        model = Collection
        exclude = ('company',)


class InvestmentForm(HTML5BootstrapModelForm):
    class Meta:
        model = Investment
        exclude = ('company',)
        widgets = {
            'share_holder': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('share:shareholder_add')}),
            'collection': forms.Select(attrs={'class': 'selectize', 'data-url': reverse_lazy('share:collection_add')}),
        }
        company_filters = ('share_holder', 'collection')
