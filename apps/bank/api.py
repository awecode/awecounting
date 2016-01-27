from rest_framework import generics
from awecounting.utils.mixins import CompanyAPI
from .models import ChequeDeposit
from .serializers import ChequeDepositSerializer


class ChequeDepositListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = ChequeDepositSerializer


class ChequeDepositDetailAPI(CompanyAPI, generics.RetrieveAPIView):
    serializer_class = ChequeDepositSerializer
