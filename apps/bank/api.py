from rest_framework import generics
from awecounting.utils.mixins import CompanyAPI
from .models import ChequeDeposit
from .serializers import ChequeDepositSerializer, BankAccountSerializer, BankCashDepositSerializer, ChequePaymentSerializer


class ChequeDepositListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = ChequeDepositSerializer


class ChequeDepositDetailAPI(CompanyAPI, generics.RetrieveAPIView):
    serializer_class = ChequeDepositSerializer


class BankAccountListAPI(CompanyAPI, generics.ListCreateAPIView):
	serializer_class = BankAccountSerializer


class BankAccountDetailAPI(CompanyAPI, generics.RetrieveAPIView):
	serializer_class = BankAccountSerializer


class BankCashDepositListAPI(CompanyAPI, generics.ListCreateAPIView):
	serializer_class = BankCashDepositSerializer


class BankCashDepositDetailAPI(CompanyAPI, generics.RetrieveAPIView):
	serializer_class = BankCashDepositSerializer


class ChequePaymentListAPI(CompanyAPI, generics.ListCreateAPIView):
	serializer_class = ChequePaymentSerializer


class ChequePaymentDetailAPI(CompanyAPI, generics.RetrieveAPIView):
	serializer_class = ChequePaymentSerializer