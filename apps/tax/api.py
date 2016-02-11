from rest_framework import generics
from awecounting.utils.mixins import CompanyAPI
from .serializers import TaxSchemeSerializer


class TaxSchemeListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = TaxSchemeSerializer


class TaxSchemeDetailAPI(CompanyAPI, generics.RetrieveAPIView):
    serializer_class = TaxSchemeSerializer
