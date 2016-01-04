from rest_framework import generics
from .models import Item, Unit
from .serializers import ItemSerializer, UnitSerializer


class ItemListAPI(generics.ListCreateAPIView):
    # queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        if self.request.company:
            queryset = queryset.filter(company=self.request.company)
        return queryset


class UnitListAPI(generics.ListCreateAPIView):
    # queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def get_queryset(self):
        queryset = Unit.objects.all()
        if self.request.company:
            queryset = queryset.filter(company=self.request.company)
        return queryset