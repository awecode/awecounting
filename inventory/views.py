from django.shortcuts import render
from inventory.models import Item, Purchase, PurchaseRow, Party
from inventory.forms import ItemForm
from inventory.serializer import PurchaseSerializer, ItemSerializer,PartySerializer
import datetime
from rest_framework import generics

def create_purchase(request, id=None):
    if id:
        purchase = get_object_or_404(Purchase, id=id)
        scenario = 'Update'
    else:
        purchase = Purchase(date=datetime.datetime.today)
        scenario = 'Create'
    data = PurchaseSerializer(purchase).data
    return render(request, 'create-purchase.html', {'data': data, 'scenario': scenario, 'purchase': purchase})



# djangorestframework API

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class PartyList(generics.ListCreateAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer


