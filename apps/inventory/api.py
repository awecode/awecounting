from rest_framework import generics

from .serializers import ItemSerializer, UnitSerializer, LocationSerializer
from awecounting.utils.mixins import CompanyAPI
from rest_framework import filters
import django_filters
from .models import Location


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
        return super(ItemListAPI, self).get_queryset().select_related('unit').select_related('ledger').select_related('account')


class UnitListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = UnitSerializer


class ProductFilter(filters.FilterSet):
    # has_item = django_filters.NumberFilter(name="contains", lookup_type='in')
    # max_price = django_filters.NumberFilter(name="price", lookup_type='lte')
    class Meta:
        model = Location
        fields = ['id', 'enabled', 'contains', 'parent']



class LocationListAPI(generics.ListCreateAPIView):
    serializer_class = LocationSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.filter(company__in=self.request.company.get_all(), enabled=True)