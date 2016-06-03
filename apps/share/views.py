from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView

from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, AjaxableResponseMixin, CompanyView, \
    AccountantMixin
from .models import ShareHolder, Collection, Investment
from .forms import ShareHolderForm, CollectionForm, InvestmentForm


class ShareHolderView(CompanyView):
    model = ShareHolder
    success_url = reverse_lazy('share:shareholder_list')
    form_class = ShareHolderForm
    check = 'can_manage_shares'


class ShareHolderList(ShareHolderView, AccountantMixin, ListView):
    pass


class ShareHolderCreate(AjaxableResponseMixin, ShareHolderView, AccountantMixin, CreateView):
    pass


class ShareHolderUpdate(ShareHolderView, AccountantMixin, UpdateView):
    pass


class ShareHolderDelete(ShareHolderView, AccountantMixin, DeleteView):
    pass


class CollectionView(CompanyView):
    model = Collection
    success_url = reverse_lazy('share:collection_list')
    form_class = CollectionForm
    check = 'can_manage_shares'


class CollectionList(CollectionView, AccountantMixin, ListView):
    pass


class CollectionCreate(AjaxableResponseMixin, CollectionView, AccountantMixin, CreateView):
    pass


class CollectionUpdate(CollectionView, AccountantMixin, UpdateView):
    pass


class CollectionDelete(CollectionView, AccountantMixin, DeleteView):
    pass


class InvestmentView(CompanyView):
    model = Investment
    success_url = reverse_lazy('share:investment_list')
    form_class = InvestmentForm
    check = 'can_manage_shares'


class InvestmentList(InvestmentView, AccountantMixin, ListView):
    pass


class InvestmentCreate(InvestmentView, AccountantMixin, CreateView):
    pass


class InvestmentUpdate(InvestmentView, AccountantMixin, UpdateView):
    pass


class InvestmentDelete(InvestmentView, AccountantMixin, DeleteView):
    pass
