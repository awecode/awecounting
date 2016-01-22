from rest_framework import generics
from .models import Item, Unit
from .serializers import ItemSerializer, UnitSerializer
from awecounting.utils.mixins import CompanyAPI


class ItemListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = ItemSerializer


class UnitListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = UnitSerializer

    def get_queryset(self):
        qs = super(UnitListAPI, self).get_queryset()
        return qs.filter(pk=39)
