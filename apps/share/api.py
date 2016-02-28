from rest_framework import generics
from awecounting.utils.mixins import CompanyAPI
from .serializers import ShareHolderSerializer, CollectionSerializer, InvestmentSerializer


class ShareHolderListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = ShareHolderSerializer


class ShareHolderDetailAPI(CompanyAPI, generics.RetrieveAPIView):
    serializer_class = ShareHolderSerializer


class CollectionListAPI(CompanyAPI, generics.ListCreateAPIView):
	serializer_class = CollectionSerializer


class CollectionDetailAPI(CompanyAPI, generics.RetrieveAPIView):
	serializer_class = CollectionSerializer


class InvestmentListAPI(CompanyAPI, generics.ListCreateAPIView):
	serializer_class = InvestmentSerializer


class InvestmentDetailAPI(CompanyAPI, generics.RetrieveAPIView):
	serializer_class = InvestmentSerializer