import json
import datetime
from datetime import timedelta

from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from rest_framework import generics
from django.db.models import Max, Q

from apps.inventory.models import Item, UnitConverter, Purchase, PurchaseRow, Party, Unit, Sale, SaleRow, JournalEntry, \
    set_transactions, InventoryAccount
from apps.inventory.forms import ItemForm, PartyForm, UnitForm, UnitConverterForm
from apps.inventory.serializer import PurchaseSerializer, ItemSerializer, PartySerializer, UnitSerializer, SaleSerializer, \
    InventoryAccountRowSerializer
from apps.ledger.models import set_transactions as set_ledger_transactions, Account, delete_rows
from awecounting.utils.mixins import DeleteView, UpdateView, CreateView, AjaxableResponseMixin, CompanyView
from awecounting.utils.helpers import save_model, invalid

from django.views.generic import ListView


def index(request):
    # import ipdb
    # ipdb.set_trace()
    objects = Sale.objects.filter(date=datetime.date.today()).prefetch_related('rows')
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
    obj = Item.objects.filter(code=code)
    if len(obj) == 1:
        item = obj[0]
        inventory_account = InventoryAccount.objects.get(item__name=item.name)
        url = reverse('view_inventory_account', kwargs={'id': inventory_account.id})
        return redirect(url)
    else:
        return render(request, 'item_search.html', {'objects': obj})


def item(request, id=None):
    if id:
        item_obj = get_object_or_404(Item, id=id)
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
                  {'form': form, 'base_template': base_template, 'scenario': scenario, 'item_data': item_obj.other_properties,
                   'item_unit_id': unit})


class ItemView(object):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('item_list')


class ItemList(ItemView, ListView):
    pass


class ItemDelete(ItemView, DeleteView):
    pass


class UnitConverterView(object):
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


def purchase_list(request):
    obj = Purchase.objects.all()
    return render(request, 'purchase_list.html', {'objects': obj})


def purchase(request, id=None):
    if id:
        purchase = get_object_or_404(Purchase, id=id)
        scenario = 'Update'
    else:
        purchase = Purchase(company=request.company)
        scenario = 'Create'
    data = PurchaseSerializer(purchase).data
    return render(request, 'purchase-form.html', {'data': data, 'scenario': scenario, 'purchase': purchase})


def save_purchase(request):
    if request.is_ajax():
        params = json.loads(request.body)
    dct = {'rows': {}}
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    object_values = {'voucher_no': params.get('voucher_no'), 'date': params.get('date'), 'party_id': params.get('party'),
                     'credit': params.get('credit'), 'company': request.company}

    if params.get('id'):
        obj = Purchase.objects.get(id=params.get('id'), company=request.company)
    else:
        obj = Purchase(company=request.company)
    # if True:
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id

        model = PurchaseRow
        for ind, row in enumerate(params.get('table_view').get('rows')):
            if invalid(row, ['item_id', 'quantity', 'unit_id']):
                continue
            else:
                values = {'sn': ind + 1, 'item_id': row.get('item')['id'], 'quantity': row.get('quantity'),
                          'rate': row.get('rate'), 'unit_id': row.get('unit_id'), 'discount': row.get('discount'),
                          'purchase': obj}
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['rows'][ind] = submodel.id
                set_transactions(submodel, obj.date,
                                 ['dr', submodel.item.account, submodel.quantity],
                                 )
                if obj.credit:
                    set_ledger_transactions(submodel, obj.date,
                                            ['cr', obj.party.account, obj.total],
                                            ['dr', submodel.item.ledger, obj.total],
                                            # ['cr', sales_tax_account, tax_amount],
                                            )
                else:
                    set_ledger_transactions(submodel, obj.date,
                                            ['dr', submodel.item.ledger, obj.total],
                                            ['cr', Account.objects.get(name='Cash', company=request.company), obj.total],
                                            # ['cr', sales_tax_account, tax_amount],
                                            )
                    delete_rows(params.get('table_view').get('deleted_rows'), model)

    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    return JsonResponse(dct)


def sale(request, id=None):
    if id:
        sale = get_object_or_404(Sale, id=id)
        scenario = 'Update'
    else:
        sale = Sale(date=datetime.datetime.now().date(), company=request.company)
        scenario = 'Create'
    data = SaleSerializer(sale).data
    return render(request, 'sale_form.html', {'data': data, 'scenario': scenario, 'sale': sale})


def save_sale(request):
    if request.is_ajax():
        params = json.loads(request.body)
    dct = {'rows': {}}
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    object_values = {'voucher_no': params.get('voucher_no'), 'date': params.get('date'), 'party_id': params.get('party'),
                     'credit': params.get('credit'), 'company': request.company}
    if params.get('id'):
        obj = Sale.objects.get(id=params.get('id'), company=request.company)
    else:
        obj = Sale(company=request.company)
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        model = SaleRow
        for ind, row in enumerate(params.get('table_view').get('rows')):
            invalid_check = invalid(row, ['item_id', 'quantity', 'unit_id'])
            if invalid_check:
                continue
                # dct['error_message'] = 'These fields must be filled: ' + ', '.join(invalid_check)
            # else:
            values = {'sn': ind + 1, 'item_id': row.get('item_id'), 'quantity': row.get('quantity'),
                      'rate': row.get('rate'), 'unit_id': row.get('unit_id'), 'discount': row.get('discount'), 'sale': obj}
            submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
            if not created:
                submodel = save_model(submodel, values)
            dct['rows'][ind] = submodel.id
            set_transactions(submodel, obj.date,
                             ['cr', submodel.item.account, submodel.quantity],
                             )
            if obj.credit:
                set_ledger_transactions(submodel, obj.date,
                                        ['cr', obj.party.account, obj.total],
                                        ['dr', 'cash', obj.total],
                                        # ['cr', sales_tax_account, tax_amount],
                                        )
            else:
                set_ledger_transactions(submodel, obj.date,
                                        ['cr', obj.party.account, obj.total],
                                        ['dr', 'cash', obj.total],
                                        # ['cr', sales_tax_account, tax_amount],
                                        )
            # delete_rows(params.get('table_view').get('deleted_rows'), model)

    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    return JsonResponse(dct)


def sale_list(request):
    objects = Sale.objects.all().prefetch_related('rows')
    return render(request, 'sale_list.html', {'objects': objects})


def sale_day(request, voucher_date):
    objects = Sale.objects.filter(date=voucher_date).prefetch_related('rows')
    total_amount = 0
    total_quantity = 0
    total_items = 0
    for obj in objects:
        for row in obj.rows.all():
            total_items += 1
            total_quantity += row.quantity
            total_amount += row.quantity * row.rate
    context = {
        'objects': objects,
        'total_amount': total_amount,
        'total_quantity': total_quantity,
        'total_items': total_items,
        'from_date': voucher_date
    }
    return render(request, 'sale_report.html', context)


def sale_date_range(request, from_date, to_date):
    objects = Sale.objects.filter(date__gte=from_date, date__lte=to_date).prefetch_related('rows')
    total_amount = 0
    total_quantity = 0
    total_items = 0
    for obj in objects:
        for row in obj.rows.all():
            total_items += 1
            total_quantity += row.quantity
            total_amount += row.quantity * row.rate
    context = {
        'objects': objects,
        'total_amount': total_amount,
        'total_quantity': total_quantity,
        'total_items': total_items,
        'from_date': from_date,
        'to_date': to_date,
    }
    return render(request, 'sale_report.html', context)


def sales_report_router(request):
    if request.GET.get('date'):
        return sale_day(request, request.GET.get('date'))
    elif request.GET.get('from') and request.GET.get('to'):
        return sale_date_range(request, request.GET.get('from'), request.GET.get('to'))
    elif request.GET.get('from'):
        return sale_day(request, request.GET.get('from'))
    else:
        return redirect(reverse_lazy('home'))


def daily_sale_today(request):
    today = datetime.date.today()
    return sale_day(request, today)


def daily_sale_yesterday(request):
    yesterday = datetime.date.today() - timedelta(1)
    return sale_day(request, yesterday)


# Party CRUD with mixins
class PartyView(object):
    model = Party
    success_url = reverse_lazy('party_list')
    form_class = PartyForm


class PartyList(PartyView, ListView):
    pass


class PartyCreate(CompanyView, AjaxableResponseMixin, PartyView, CreateView):
    pass


class PartyUpdate(CompanyView, PartyView, UpdateView):
    def form_valid(self, form):
        form.instance.company = self.request.company
        return super(PartyUpdate, self).form_valid(form)


class PartyDelete(PartyView, DeleteView):
    pass


# Unit CRUD with mixins
class UnitView(object):
    model = Unit
    success_url = reverse_lazy('unit_list')
    form_class = UnitForm


class UnitList(UnitView, ListView):
    pass


class UnitCreate(AjaxableResponseMixin, UnitView, CreateView):
    def form_valid(self, form):
        form.instance.company = self.request.company
        return super(UnitCreate, self).form_valid(form)


class UnitUpdate(UnitView, UpdateView):
    def form_valid(self, form):
        form.instance.company = self.request.company
        return super(UnitUpdate, self).form_valid(form)


class UnitDelete(UnitView, DeleteView):
    pass


def list_inventory_accounts(request):
    objects = InventoryAccount.objects.all()
    return render(request, 'list_inventory_accounts.html', {'objects': objects})


def view_inventory_account(request, id):
    obj = get_object_or_404(InventoryAccount, id=id)
    if hasattr(obj, 'item'):
        if request.POST:
            unit = Unit.objects.get(pk=request.POST.get('unit_id'))
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
                  {'obj': obj, 'entries': journal_entries, 'unit_conversions': conversions, 'unit': unit, 'multiple': multiple})


def view_inventory_account_with_rate(request, id):
    obj = get_object_or_404(InventoryAccount, id=id)
    # units = Unit.objects.all()
    units_to_convert = UnitConverter.objects.filter(base_unit__name=obj.item.unit.name).values_list('unit_to_convert__pk',
                                                                                                    flat=True)
    units_to_convert_list = Unit.objects.filter(pk__in=units_to_convert)
    units_list = [o for o in units_to_convert_list]
    units_list.append(Unit.objects.get(pk=obj.item.unit.pk))
    if request.POST:
        unit_id = request.POST.get('unit-convert-option')
        unit = Unit.objects.get(pk=unit_id)
        if unit.name != obj.item.unit.name:
            unit_convert = UnitConverter.objects.get(base_unit__name=obj.item.unit.name, unit_to_convert__name=unit.name)
            multiple = unit_convert.multiple
            journal_entries = JournalEntry.objects.filter(transactions__account_id=obj.id).order_by('id', 'date') \
                .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
            data = InventoryAccountRowSerializer(journal_entries, many=True,
                                                 context={'unit_multiple': multiple, 'default_unit': obj.item.unit.name}).data
            current_unit = unit.name
            return render(request, 'inventory_account_detail_with_rate.html',
                          {'obj': obj, 'entries': journal_entries, 'data': data, 'units': units_list,
                           'current_unit': current_unit})
    journal_entries = JournalEntry.objects.filter(transactions__account_id=obj.id).order_by('id', 'date') \
        .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
    data = InventoryAccountRowSerializer(journal_entries, many=True, context={'default_unit': obj.item.unit.name}).data
    current_unit = obj.item.unit
    return render(request, 'inventory_account_detail_with_rate.html',
                  {'obj': obj, 'entries': journal_entries, 'data': data, 'units': units_list, 'current_unit': current_unit})

