import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .serializers import ItemSerializer, InventoryAccountRowSerializer
from ..voucher.models import Sale
from .models import Item, UnitConversion, Unit, JournalEntry, InventoryAccount
from .forms import ItemForm, UnitForm, UnitConversionForm
from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, AjaxableResponseMixin, CompanyView


@login_required
def index(request):
    objects = Sale.objects.filter(company=request.company, date=datetime.date.today()).prefetch_related('rows')
    total_amount = 0
    total_quantity = 0
    total_items = 0
    for obj in objects:
        for row in obj.rows.all():
            total_items += 1
            total_quantity += row.quantity
            total_amount += row.quantity * row.rate
    context = {
        'total_amount': total_amount,
        'total_quantity': total_quantity,
        'total_items': total_items,
    }
    return render(request, 'index.html', context)


def item_search(request):
    code = request.POST.get('search-code')
    obj = Item.objects.filter(code=code, company=request.company)
    if not obj:
        obj = Item.objects.filter(name=code, company=request.company)
    if len(obj) == 1:
        itm = obj[0]
        inventory_account = InventoryAccount.objects.get(item__name=itm.name, company=request.company)
        url = reverse('view_inventory_account', kwargs={'pk': inventory_account.id})
        return redirect(url)
    else:
        return render(request, 'item_search.html', {'objects': obj})


def item(request, pk=None):
    if pk:
        item_obj = get_object_or_404(Item, id=pk, company=request.company)
        scenario = 'Update'
        unit = item_obj.unit.id
    else:
        item_obj = Item()
        scenario = 'Create'
        unit = ''
    if request.POST:
        form = ItemForm(data=request.POST, instance=item_obj, request=request)
        if form.is_valid():
            item_obj = form.save(commit=False)
            property_name = request.POST.getlist('property_name')
            item_property = request.POST.getlist('property')
            unit_id = request.POST.get('unit')
            item_obj.unit_id = int(unit_id)
            item_obj.company = request.company
            if request.FILES != {}:
                item_obj.image = request.FILES['image']
            other_properties = {}
            for key, value in zip(property_name, item_property):
                if key and value:
                    other_properties[key] = value
            if other_properties: item_obj.other_properties = other_properties
            item_obj.save(account_no=form.cleaned_data['account_no'])
            if request.is_ajax():
                return JsonResponse(ItemSerializer(item_obj).data)
            return redirect(reverse('item_list'))
    else:
        form = ItemForm(instance=item_obj, request=request)
    if request.is_ajax():
        base_template = '_modal.html'
    else:
        base_template = '_base.html'
    return render(request, 'item_form.html',
                  {'form': form, 'base_template': base_template, 'scenario': scenario,
                   'item_data': item_obj.other_properties,
                   })


class ItemView(CompanyView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('item_list')


# def form_valid(self, form):
#         self.object = form.save(commit=False)
#         property_name = self.request.POST.getlist('property_name')
#         item_property = self.request.POST.getlist('property')
#         unit_id = self.request.POST.get('unit')
#         self.object.unit_id = int(unit_id)
#         self.object.company = self.request.company
#         if self.request.FILES != {}:
#             self.object.image = self.request.FILES['image']
#         other_properties = {}
#         for key, value in zip(property_name, item_property):
#             if key and value:
#                 other_properties[key] = value
#         if other_properties: self.object.other_properties = other_properties
#         self.object.save(account_no=form.cleaned_data['account_no'])
#         return super(ItemView, self).form_valid(form)
# 
# 
# class ItemCreate(StaffMixin, ItemView, AjaxableResponseMixin, CreateView):
#     def get_context_data(self, *args, **kwargs):
#         data = super(ItemCreate, self).get_context_data(*args, **kwargs)
#         # data['item_data'] = self.object.other_properties
#         return data
# 
# 
# class ItemUpdate(StaffMixin, ItemView, AjaxableResponseMixin, UpdateView):
#     def get_context_data(self, *args, **kwargs):
#         data = super(ItemUpdate, self).get_context_data(*args, **kwargs)
#         # data['item_data'] = self.object.other_properties
#         # data['item_unit_id'] = self.object.unit_id
#         return data


class ItemList(ItemView, ListView):
    pass


class ItemDelete(ItemView, DeleteView):
    pass


class UnitConversionView(CompanyView):
    model = UnitConversion
    form_class = UnitConversionForm
    success_url = reverse_lazy('unit_conversion_list')


class UnitConversionList(UnitConversionView, ListView):
    pass


class UnitConversionCreate(UnitConversionView, CreateView):
    pass


class UnitConversionUpdate(UnitConversionView, UpdateView):
    pass


class UnitConversionDelete(UnitConversionView, DeleteView):
    pass


# Unit CRUD with mixins
class UnitView(CompanyView):
    model = Unit
    success_url = reverse_lazy('unit_list')
    form_class = UnitForm


class UnitList(UnitView, ListView):
    pass


class UnitCreate(AjaxableResponseMixin, UnitView, CreateView):
    pass


class UnitUpdate(UnitView, UpdateView):
    pass


class UnitDelete(UnitView, DeleteView):
    pass


class InventoryAccountView(CompanyView):
    model = InventoryAccount
    template_name = 'list_inventory_accounts.html'


class InventoryAccountList(InventoryAccountView, ListView):
    def get_queryset(self):
        return self.model.objects.order_by('-item')


# def list_inventory_accounts(request):
#     objects = InventoryAccount.objects.filter(company=request.company).order_by('-item')
#     return render(request, 'list_inventory_accounts.html', {'objects': objects})

class InventoryAccountDetail(InventoryAccountView, DetailView):
    template_name = 'inventory_account_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(InventoryAccountDetail, self).get_context_data(*args, **kwargs)
        self.object = self.get_object()
        if hasattr(self.object, 'item'):
            if self.request.POST:
                unit = Unit.objects.get(pk=self.request.POST.get('unit_id'), company=self.request.company)
            else:
                unit = self.object.item.unit
        else:
            unit = None
        journal_entries = JournalEntry.objects.filter(transactions__account_id=self.object.id).order_by('id', 'date') \
            .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
        conversions = UnitConversion.objects.filter(Q(base_unit=unit) | Q(unit_to_convert=unit)).select_related(
            'base_unit',
            'unit_to_convert')
        multiple = 1
        if hasattr(self.object, 'item'):
            if not unit == self.object.item.unit:
                if conversions.filter(base_unit=unit).first():
                    multiple = 1 / conversions.filter(base_unit=unit).first().multiple
                elif conversions.filter(unit_to_convert=unit).first():
                    multiple = conversions.filter(unit_to_convert=unit).first().multiple
        context['entries'] = journal_entries
        context['unit_conversions'] = conversions
        context['unit'] = unit
        context['multiple'] = multiple
        return context


# def view_inventory_account(request, pk):
#     obj = get_object_or_404(InventoryAccount, pk=pk, company=request.company)
#     if hasattr(obj, 'item'):
#         if request.POST:
#             unit = Unit.objects.get(pk=request.POST.get('unit_id'), company=request.company)
#         else:
#             unit = obj.item.unit
#     else:
#         unit = None
#     journal_entries = JournalEntry.objects.filter(transactions__account_id=obj.id).order_by('id', 'date') \
#         .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
#     conversions = UnitConversion.objects.filter(Q(base_unit=unit) | Q(unit_to_convert=unit)).select_related('base_unit',
#                                                                                                             'unit_to_convert')
#     multiple = 1
#     if hasattr(obj, 'item'):
#         if not unit == obj.item.unit:
#             if conversions.filter(base_unit=unit).first():
#                 multiple = 1 / conversions.filter(base_unit=unit).first().multiple
#             elif conversions.filter(unit_to_convert=unit).first():
#                 multiple = conversions.filter(unit_to_convert=unit).first().multiple
#     return render(request, 'inventory_account_detail.html',
#                   {'obj': obj, 'entries': journal_entries, 'unit_conversions': conversions, 'unit': unit,
#                    'multiple': multiple})

class InventoryAccountWithRate(InventoryAccountView, DetailView):
    template_name = 'inventory_account_detail_with_rate.html'

    def get_context_data(self, *args, **kwargs):
        context = super(InventoryAccountWithRate, self).get_context_data(*args, **kwargs)
        self.object = self.get_object()
        if hasattr(self.object, 'item'):
            if self.request.POST:
                unit = Unit.objects.get(pk=self.request.POST.get('unit_id'), company=self.request.company)
            else:
                unit = self.object.item.unit
        else:
            unit = None
        conversions = UnitConversion.objects.filter(Q(base_unit=unit) | Q(unit_to_convert=unit)).select_related(
            'base_unit',
            'unit_to_convert')
        multiple = 1
        journal_entries = JournalEntry.objects.filter(transactions__account_id=self.object.id).order_by('id', 'date') \
            .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
        data = InventoryAccountRowSerializer(journal_entries, many=True,
                                             context={'default_unit': self.object.item.unit.name}).data
        context['entries'] = journal_entries
        context['data'] = data
        context['unit_conversions'] = conversions
        context['unit'] = unit
        context['multiple'] = multiple
        return context

# def view_inventory_account_with_rate(request, pk):
#     obj= get_object_or_404(InventoryAccount, pk=pk, company=request.company)
#     if hasattr(obj, 'item'):
#         if request.POST:
#             unit = Unit.objects.get(pk=request.POST.get('unit_id'), company=request.company)
#         else:
#             unit = obj.item.unit
#     else:
#         unit = None
#     conversions = UnitConversion.objects.filter(Q(base_unit=unit) | Q(unit_to_convert=unit)).select_related('base_unit',
#                                                                                                             'unit_to_convert')
#     multiple = 1
#     journal_entries = JournalEntry.objects.filter(transactions__account_id=obj.id).order_by('id', 'date') \
#         .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
#     data = InventoryAccountRowSerializer(journal_entries, many=True, context={'default_unit': obj.item.unit.name}).data
#
#     return render(request, 'inventory_account_detail_with_rate.html',
#                   {'obj': obj, 'entries': journal_entries, 'data': data, 'unit_conversions': conversions, 'unit': unit,
#                    'multiple': multiple})
