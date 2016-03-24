from rest_framework import generics
from .models import Item, Unit
from .serializers import ItemSerializer, UnitSerializer
from awecounting.utils.mixins import CompanyAPI


class ItemListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
    	if self.kwargs.get('pk'):
    		return self.serializer_class.Meta.model.objects.filter(company_id=self.kwargs.get('pk'))
        return super(ItemListAPI, self).get_queryset()


class UnitListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = UnitSerializer
