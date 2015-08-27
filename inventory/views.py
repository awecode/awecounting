from django.shortcuts import render
from inventory.models import Purchase

def create_purchase(request):
	import ipdb; ipdb.set_trace()
	obj = Purchase.objects.all()
	return render(request, 'create-purchase.html')
# Create your views here.
