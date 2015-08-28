import json
from django.shortcuts import render, get_object_or_404
from inventory.models import Item, Purchase, PurchaseRow, Party, Unit, Sale, SaleRow
from inventory.forms import ItemForm
from django.http import JsonResponse, HttpResponse
from inventory.serializer import PurchaseSerializer, ItemSerializer, PartySerializer, UnitSerializer, SaleSerializer
import datetime
from rest_framework import generics

def save_model(model, values):
    for key, value in values.items():
        setattr(model, key, value)
    model.save()
    return model

def invalid(row, required_fields):
    invalid_attrs = []
    for attr in required_fields:
        # if one of the required attributes isn't received or is an empty string
        if not attr in row or row.get(attr) == "":
            invalid_attrs.append(attr)
    if len(invalid_attrs) is 0:
        return False
    return invalid_attrs

def purchase_list(request):
	obj = Purchase.objects.all()
	return render(request, 'purchase_list.html', {'objects': obj})

def purchase(request, id=None):
    if id:
        purchase = get_object_or_404(Purchase, id=id)
        scenario = 'Update'
    else:
        purchase = Purchase(date=datetime.datetime.now().date())
        scenario = 'Create'
    data = PurchaseSerializer(purchase).data
    return render(request, 'create-purchase.html', {'data': data, 'scenario': scenario, 'purchase': purchase})

def save_purchase(request):
    if request.is_ajax():
        params = json.loads(request.body)
    dct= {'rows': {}}
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    object_values = {'voucher_no': params.get('voucher_no'), 'date': params.get('date'), 'party_id': params.get('party')}
    if params.get('id'):
        obj = Purchase.objects.get(id=params.get('id'))
    else:
        obj = Purchase()
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        model = PurchaseRow
        for index, row in enumerate(params.get('table_view').get('rows')):
            invalid_check = invalid(row, ['item_id', 'quantity', 'unit_id'])
            if invalid_check:
                dct['error_message'] = 'These feilds must be filled: ' + ', '.join(invalid_check)
                return JsonResponse(dct)
            else:
                values = {'sn': index+1, 'item_id': row.get('item_id'), 'quantity': row.get('quantity'),
                    'rate': row.get('rate'), 'unit_id': row.get('unit_id'), 'purchase': obj }
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['rows'][index] = submodel.id
        # delete_rows(params.get('table_view').get('deleted_rows'), model)

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
        sale = Sale(date=datetime.datetime.now().date())
        scenario = 'Create'
    data = SaleSerializer(sale).data
    return render(request, 'create-sale.html', {'data': data, 'scenario': scenario, 'sale': sale})

def save_sale(request):
    if request.is_ajax():
        params = json.loads(request.body)
    dct= {'rows': {}}
    if params.get('voucher_no') == '':
        params['voucher_no'] = None
    object_values = {'voucher_no': params.get('voucher_no'), 'date': params.get('date'), 'party_id': params.get('party')}
    if params.get('id'):
        obj = Sale.objects.get(id=params.get('id'))
    else:
        obj = Sale()
    try:
        obj = save_model(obj, object_values)
        dct['id'] = obj.id
        model = SaleRow
        for index, row in enumerate(params.get('table_view').get('rows')):
            invalid_check = invalid(row, ['item_id', 'quantity', 'unit_id'])
            if invalid_check:
                dct['error_message'] = 'These feilds must be filled: ' + ', '.join(invalid_check)
                return JsonResponse(dct)
            else:
                values = {'sn': index+1, 'item_id': row.get('item_id'), 'quantity': row.get('quantity'),
                    'rate': row.get('rate'), 'unit_id': row.get('unit_id'), 'sale': obj }
                submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
                if not created:
                    submodel = save_model(submodel, values)
                dct['rows'][index] = submodel.id
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
    obj = Sale.objects.all()
    return render(request, 'sale_list.html', {'objects': obj})


# djangorestframework API

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class UnitList(generics.ListCreateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class PartyList(generics.ListCreateAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer


