from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from awecounting.utils.mixins import DeleteView, UpdateView, CreateView
from .models import ShareHolder, Collection, Investment
from .forms import ShareHolderForm, CollectionForm, InvestmentForm
import json


class ShareHolderView(object):
    model = ShareHolder
    success_url = reverse_lazy('share:shareholder_list')
    form_class = ShareHolderForm


class ShareHolderList(ShareHolderView, ListView):
    pass


class ShareHolderCreate(ShareHolderView, CreateView):
    pass


class ShareHolderUpdate(ShareHolderView, UpdateView):
    pass


class ShareHolderDelete(ShareHolderView, DeleteView):
    pass



class CollectionView(object):
    model = Collection
    success_url = reverse_lazy('share:collection_list')
    form_class = CollectionForm


class CollectionList(CollectionView, ListView):
    pass


class CollectionCreate(CollectionView, CreateView):
    pass


class CollectionUpdate(CollectionView, UpdateView):
    pass


class CollectionDelete(CollectionView, DeleteView):
    pass


class InvestmentView(object):
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
