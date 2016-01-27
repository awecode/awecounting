from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, AjaxableResponseMixin, CompanyView, AccountantMixin, StaffMixin
from .models import TaxScheme
from .forms import TaxSchemeForm


class TaxSchemeView(CompanyView):
    model = TaxScheme
    success_url = reverse_lazy('tax_scheme_list')
    form_class = TaxSchemeForm


class TaxSchemeList(TaxSchemeView, StaffMixin, ListView):
    pass


class TaxSchemeCreate(AjaxableResponseMixin, AccountantMixin, TaxSchemeView, CreateView):
    pass


class TaxSchemeUpdate(TaxSchemeView, AccountantMixin, UpdateView):
    pass


class TaxSchemeDelete(TaxSchemeView, AccountantMixin, DeleteView):
    pass


# Create your views here.
