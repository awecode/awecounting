from rest_framework import generics

from .serializers import ItemSerializer, UnitSerializer
from awecounting.utils.mixins import CompanyAPI


class ItemListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = ItemSerializer

    def get_serializer_context(self):
        context = super(ItemListAPI, self).get_serializer_context()
        context['voucher'] = self.kwargs.get('voucher')
        return context

    def get_queryset(self):
        if self.kwargs.get('pk'):
            # TODO Security
            return self.serializer_class.Meta.model.objects.filter(company_id=self.kwargs.get('pk'))
        return super(ItemListAPI, self).get_queryset()


class UnitListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = UnitSerializer
