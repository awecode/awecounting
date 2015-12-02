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

    def form_valid(self, form):
        form.instance.company = self.request.company
        return super(ShareHolderCreate, self).form_valid(form)


class ShareHolderUpdate(ShareHolderView, UpdateView):

    def form_valid(self, form):
        form.instance.company = self.request.company
        return super(ShareHolderUpdate, self).form_valid(form)



class ShareHolderDelete(ShareHolderView, DeleteView):
    pass



class CollectionView(object):
    model = Collection
    success_url = reverse_lazy('share:collection_list')
    form_class = CollectionForm


class CollectionList(CollectionView, ListView):
    pass


class CollectionCreate(CollectionView, CreateView):

    def form_valid(self, form):
        form.instance.company = self.request.company
        return super(CollectionCreate, self).form_valid(form)



class CollectionUpdate(CollectionView, UpdateView):

    def form_valid(self, form):
        form.instance.company = self.request.company
        return super(CollectionUpdate, self).form_valid(form)



class CollectionDelete(CollectionView, DeleteView):
    pass


class InvestmentView(object):
    model = Investment
    success_url = reverse_lazy('share:investment_list')
    form_class = InvestmentForm


class InvestmentList(InvestmentView, ListView):
    pass


class InvestmentCreate(InvestmentView, CreateView):
  
    def form_valid(self, form):
        form.instance.company = self.request.company
        return super(InvestmentCreate, self).form_valid(form)



class InvestmentUpdate(InvestmentView, UpdateView):
    
    def form_valid(self, form):
        form.instance.company = self.request.company
        return super(InvestmentUpdate, self).form_valid(form)



class InvestmentDelete(InvestmentView, DeleteView):
    pass
