from rest_framework import generics
from awecounting.utils.mixins import CompanyAPI
from .models import Account, Party
from .serializers import AccountSerializer, PartySerializer, PartyBalanceSerializer


class AccountListAPI(generics.ListCreateAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = Account.objects.all()
        if 'category' in self.kwargs:
            category_name = self.kwargs['category'].replace('_', ' ').title()
            queryset = queryset.filter(category__name=category_name)
        return queryset


class PartyListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = PartySerializer


class PartyBalanceListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = PartyBalanceSerializer
