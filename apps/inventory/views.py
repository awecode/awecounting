import datetime
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import ListView

from .serializers import ItemSerializer, InventoryAccountRowSerializer
from ..voucher.models import Sale
from .models import Item, UnitConverter, Unit, JournalEntry, InventoryAccount
from .forms import ItemForm, UnitForm, UnitConverterForm
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
    if len(obj) == 1:
        itm = obj[0]
        inventory_account = InventoryAccount.objects.get(item__name=itm.name, company=request.company)
        url = reverse('view_inventory_account', kwargs={'id': inventory_account.id})
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
        form = ItemForm(data=request.POST, instance=item_obj)
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
                other_properties[key] = value
            item_obj.other_properties = other_properties
            item_obj.save(account_no=form.cleaned_data['account_no'])
            if request.is_ajax():
                return JsonResponse(ItemSerializer(item_obj).data)
            return redirect('/inventory/item')
    else:
        form = ItemForm(instance=item_obj)
    if request.is_ajax():
        base_template = '_modal.html'
    else:
        base_template = '_base.html'
    return render(request, 'item_form.html',
                  {'form': form, 'base_template': base_template, 'scenario': scenario,
                   'item_data': item_obj.other_properties,
                   'item_unit_id': unit})


class ItemView(CompanyView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('item_list')


class ItemList(ItemView, ListView):
    pass


class ItemDelete(ItemView, DeleteView):
    pass


class UnitConverterView(CompanyView):
    model = UnitConverter
    form_class = UnitConverterForm
    success_url = reverse_lazy('unitconverter_list')


class UnitConverterList(UnitConverterView, ListView):
    pass


class UnitConverterCreate(UnitConverterView, CreateView):
    pass


class UnitConverterUpdate(UnitConverterView, UpdateView):
    pass


class UnitConverterDelete(UnitConverterView, DeleteView):
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


def list_inventory_accounts(request):
    objects = InventoryAccount.objects.filter(company=request.company)
    return render(request, 'list_inventory_accounts.html', {'objects': objects})


def view_inventory_account(request, id):
    obj = get_object_or_404(InventoryAccount, id=id, company=request.company)
    if hasattr(obj, 'item'):
        if request.POST:
            unit = Unit.objects.get(pk=request.POST.get('unit_id'), company=request.company)
        else:
            unit = obj.item.unit
    else:
        unit = None
    journal_entries = JournalEntry.objects.filter(transactions__account_id=obj.id).order_by('id', 'date') \
        .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
    conversions = UnitConverter.objects.filter(Q(base_unit=unit) | Q(unit_to_convert=unit)).select_related('base_unit',
                                                                                                           'unit_to_convert')
    multiple = 1
    if hasattr(obj, 'item'):
        if not unit == obj.item.unit:
            if conversions.filter(base_unit=unit).first():
                multiple = 1 / conversions.filter(base_unit=unit).first().multiple
            elif conversions.filter(unit_to_convert=unit).first():
                multiple = conversions.filter(unit_to_convert=unit).first().multiple
    return render(request, 'inventory_account_detail.html',
                  {'obj': obj, 'entries': journal_entries, 'unit_conversions': conversions, 'unit': unit,
                   'multiple': multiple})


def view_inventory_account_with_rate(request, id):
    obj = get_object_or_404(InventoryAccount, id=id, company=request.company)
    # units = Unit.objects.all()
    units_to_convert = UnitConverter.objects.filter(base_unit__name=obj.item.unit.name).values_list(
        'unit_to_convert__pk',
        flat=True)
    units_to_convert_list = Unit.objects.filter(pk__in=units_to_convert)
    units_list = [o for o in units_to_convert_list]
    units_list.append(Unit.objects.get(pk=obj.item.unit.pk))
    if request.POST:
        unit_id = request.POST.get('unit-convert-option')
        unit = Unit.objects.get(pk=unit_id)
        if unit.name != obj.item.unit.name:
            unit_convert = UnitConverter.objects.get(base_unit__name=obj.item.unit.name,
                                                     unit_to_convert__name=unit.name)
            multiple = unit_convert.multiple
            journal_entries = JournalEntry.objects.filter(transactions__account_id=obj.id).order_by('id', 'date') \
                .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
            data = InventoryAccountRowSerializer(journal_entries, many=True,
                                                 context={'unit_multiple': multiple,
                                                          'default_unit': obj.item.unit.name}).data
            current_unit = unit.name
            return render(request, 'inventory_account_detail_with_rate.html',
                          {'obj': obj, 'entries': journal_entries, 'data': data, 'units': units_list,
                           'current_unit': current_unit})
    journal_entries = JournalEntry.objects.filter(transactions__account_id=obj.id).order_by('id', 'date') \
        .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
    data = InventoryAccountRowSerializer(journal_entries, many=True, context={'default_unit': obj.item.unit.name}).data
    current_unit = obj.item.unit
    return render(request, 'inventory_account_detail_with_rate.html',
                  {'obj': obj, 'entries': journal_entries, 'data': data, 'units': units_list,
                   'current_unit': current_unit})
