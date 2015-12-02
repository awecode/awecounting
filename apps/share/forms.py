from awecounting.utils.forms import HTML5BootstrapModelForm
from .models import ShareHolder, Collection, Investment


class ShareHolderForm(HTML5BootstrapModelForm):
    class Meta:
        model = ShareHolder
        exclude = ()


class CollectionForm(HTML5BootstrapModelForm):
    class Meta:
        model = Collection
        exclude = ()


class InvestmentForm(HTML5BootstrapModelForm):
    class Meta:
        model = Investment
        exclude = ()
