from django.shortcuts import render
from inventory.models import Purchase, Purchase, PurchaseRow
from inventory.forms import ItemForm
from inventory.serializer import PurchaseSerializer
import datetime
def create_purchase(request, id=None):
    if id:
        purchase = get_object_or_404(Purchase, id=id)
        scenario = 'Update'
    else:
        purchase = Purchase(date=datetime.datetime.today)
        scenario = 'Create'
    data = PurchaseSerializer(purchase).data
    return render(request, 'create-purchase.html', {'data': data, 'scenario': scenario, 'purchase': purchase})
