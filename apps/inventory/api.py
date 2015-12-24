from rest_framework import generics
from .models import Item, Unit, Party
from .serializer import ItemSerializer, PartySerializer, UnitSerializer


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


class PartyListAPI(generics.ListCreateAPIView):
    # queryset = Party.objects.all()
    serializer_class = PartySerializer

    def get_queryset(self):
        queryset = Party.objects.all()
        if self.request.company:
            queryset = queryset.filter(company=self.request.company)
        return queryset
