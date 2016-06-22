from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy

from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, AjaxableResponseMixin, CompanyView, \
    AccountantMixin, StockistCashierMixin, ListView
from .models import Party, Category, Account, JournalEntry
from .forms import PartyForm, AccountForm, CategoryForm


class ViewAccount(AccountantMixin, ListView):
    model = Account
    template_name = 'view_ledger.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ViewAccount, self).get_context_data(**kwargs)
        base_template = 'dashboard.html'
        pk = int(self.kwargs.get('pk'))
        obj = get_object_or_404(self.model, pk=pk, company__in=self.request.company.get_all())
        journal_entries = JournalEntry.objects.filter(transactions__account_id=obj.pk).order_by('pk',
                                                                                                'date') \
            .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
        context['account'] = obj
        context['journal_entries'] = journal_entries
        context['base_template'] = base_template
        return context


class CategoryView(CompanyView):
    model = Category
    success_url = reverse_lazy('category_list')
    form_class = CategoryForm

    def get_form(self, form_class=None):
        kwargs = self.get_form_kwargs()
        kwargs['request'] = self.request
        return self.form_class(**kwargs)


class CategoryList(CategoryView, AccountantMixin, ListView):
    pass


class CategoryCreate(AjaxableResponseMixin, CategoryView, AccountantMixin, CreateView):
    pass


class CategoryUpdate(CategoryView, AccountantMixin, UpdateView):
    pass


class CategoryDelete(CategoryView, AccountantMixin, DeleteView):
    pass


# Party CRUD with mixins
class PartyView(CompanyView):
    model = Party
    success_url = reverse_lazy('party_list')
    form_class = PartyForm

    def form_valid(self, form):
        if self.request.POST.get('related_company'):
            form.instance.related_company_id = int(self.request.POST.get('related_company'))
        return super(PartyView, self).form_valid(form)


class PartyList(PartyView, StockistCashierMixin, ListView):
    pass


class PartyCreate(AjaxableResponseMixin, PartyView, StockistCashierMixin, CreateView):
    def get_initial(self):
        dct = {}
        if self.request.GET and 'source' in self.request.GET:
            if self.request.GET['source'] == 'purchase':
                dct['type'] = 'Supplier'
            elif self.request.GET['source'] == 'sale':
                dct['type'] = 'Customer'
        return dct


class PartyUpdate(PartyView, StockistCashierMixin, UpdateView):
    pass


class PartyDelete(PartyView, StockistCashierMixin, DeleteView):
    pass


class AccountView(CompanyView):
    model = Account
    success_url = reverse_lazy('account_list')
    form_class = AccountForm
    search_fields = ['name', 'company__name', 'category__name']

    def get_initial(self):
        dct = super(AccountView, self).get_initial()
        if self.request.GET.get('fy'):
            dct['fy'] = int(self.request.GET.get('fy')) or self.request.company.fy
        if self.request.GET.get('category'):
            category_name = self.request.GET['category'].replace('_', ' ').title()
            category = Category.objects.filter(name=category_name).first()
            dct['category'] = category
        return dct
    
class AccountTree(CategoryView, AccountantMixin, ListView):
    template_name = 'ledger/account_tree.html'
    
    def get_queryset(self):
        qs = super(AccountTree, self).get_queryset()
        qs = qs.prefetch_related('accounts')
        return qs


class AccountList(AccountView, AccountantMixin, ListView):
    pass


class AccountCreate(AjaxableResponseMixin, AccountView, AccountantMixin, CreateView):
    pass


class AccountUpdate(AccountView, AccountantMixin, UpdateView):
    pass


class AccountDelete(AccountView, AccountantMixin, DeleteView):
    pass
