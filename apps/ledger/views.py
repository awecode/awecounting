from django.shortcuts import render, get_object_or_404

from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, AjaxableResponseMixin, CompanyView
from .models import Party, Category, Account, JournalEntry
from .forms import PartyForm, AccountForm, CategoryForm


# TODO Roshan - Convert following view methods to class based views

def view_account(request, id):
    account = get_object_or_404(Account, id=id, company=request.company)
    # transactions = account.transactions
    base_template = 'dashboard.html'
    journal_entries = JournalEntry.objects.filter(transactions__account_id=account.id).order_by('id',
                                                                                                'date') \
        .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
    return render(request, 'view_account.html', {
        'account': account,
        # 'transactions': transactions.all(),
        'journal_entries': journal_entries,
        'base_template': base_template,
    })


class CategoryView(CompanyView):
    model = Category
    success_url = reverse_lazy('category_list')
    form_class = CategoryForm

class CategoryList(CategoryView, ListView):
    pass


class CategoryCreate(AjaxableResponseMixin, CategoryView, CreateView):
    pass


class CategoryUpdate(CategoryView, UpdateView):
    pass


class CategoryDelete(CategoryView, DeleteView):
    pass



# Party CRUD with mixins
class PartyView(CompanyView):
    model = Party
    success_url = reverse_lazy('party_list')
    form_class = PartyForm


class PartyList(PartyView, ListView):
    pass


class PartyCreate(AjaxableResponseMixin, PartyView, CreateView):
    pass


class PartyUpdate(PartyView, UpdateView):
    pass


class PartyDelete(PartyView, DeleteView):
    pass


class AccountView(CompanyView):
    model = Account
    success_url = reverse_lazy('account_list')
    form_class = AccountForm


class AccountList(AccountView, ListView):
    pass


class AccountCreate(AjaxableResponseMixin, AccountView, CreateView):
    pass


class AccountUpdate(AccountView, UpdateView):
    pass


class AccountDelete(AccountView, DeleteView):
    pass
