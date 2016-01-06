from rest_framework import generics
from .models import Account, Party
from .serializers import AccountSerializer, PartySerializer, PartyBalanceSerializer


class AccountListAPI(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    # queryset = Account.objects.all()

    def get_queryset(self):
        queryset = Account.objects.all()
        if 'category' in self.kwargs:
            category_name = self.kwargs['category'].replace('_', ' ').title()
            queryset = queryset.filter(category__name=category_name)
        return queryset

class PartyListAPI(generics.ListCreateAPIView):
    # queryset = Party.objects.all()
    serializer_class = PartySerializer

    def get_queryset(self):
        queryset = Party.objects.all()
        if self.request.company:
            queryset = queryset.filter(company=self.request.company)
        return queryset

class PartyBalanceListAPI(generics.ListCreateAPIView):
    # queryset = Party.objects.all()
    serializer_class = PartyBalanceSerializer

    def get_queryset(self):
        queryset = Party.objects.all()
        if self.request.company:
            queryset = queryset.filter(company=self.request.company)
        return queryset
