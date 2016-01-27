from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, AjaxableResponseMixin, CompanyView
from .models import ShareHolder, Collection, Investment
from .forms import ShareHolderForm, CollectionForm, InvestmentForm


class ShareHolderView(CompanyView):
    model = ShareHolder
    success_url = reverse_lazy('share:shareholder_list')
    form_class = ShareHolderForm


class ShareHolderList(ShareHolderView, ListView):
    pass


class ShareHolderCreate(AjaxableResponseMixin, ShareHolderView, CreateView):
    pass


class ShareHolderUpdate(ShareHolderView, UpdateView):
    pass


class ShareHolderDelete(ShareHolderView, DeleteView):
    pass


class CollectionView(CompanyView):
    model = Collection
    success_url = reverse_lazy('share:collection_list')
    form_class = CollectionForm


class CollectionList(CollectionView, ListView):
    pass


class CollectionCreate(AjaxableResponseMixin, CollectionView, CreateView):
    pass


class CollectionUpdate(CollectionView, UpdateView):
    pass


class CollectionDelete(CollectionView, DeleteView):
    pass


class InvestmentView(CompanyView):
    model = Investment
    success_url = reverse_lazy('share:investment_list')
    form_class = InvestmentForm


class InvestmentList(InvestmentView, ListView):
    pass


class InvestmentCreate(InvestmentView, CreateView):
    pass


class InvestmentUpdate(InvestmentView, UpdateView):
    pass


class InvestmentDelete(InvestmentView, DeleteView):
    pass
