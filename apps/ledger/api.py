from rest_framework import generics
from awecounting.utils.mixins import CompanyAPI
from .models import Account
from .serializers import AccountSerializer, PartySerializer, PartyBalanceSerializer, CategorySerializer


class AccountListAPI(generics.ListCreateAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = Account.objects.filter(company=self.request.company)
        if 'category' in self.kwargs:
            category_name = self.kwargs['category'].replace('_', ' ').title()
            queryset = queryset.filter(category__name=category_name)
        if 'categories' in self.request.query_params:
            categories = self.request.query_params['categories'].split(',')
            categories = [category.replace('_', ' ').title() for category in categories]
            queryset = queryset.filter(category__name__in=categories)
        return queryset


class PartyListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = PartySerializer


class PartyBalanceListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = PartyBalanceSerializer


class CategoryListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = CategorySerializer


class CategoryDetailAPI(CompanyAPI, generics.RetrieveAPIView):
    serializer_class = CategorySerializer
