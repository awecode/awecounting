from rest_framework import generics
from .serializers import SaleSerializer, PurchaseSerializer
from .models import Sale, CashReceipt, Purchase


class PendingSaleListAPI(generics.ListCreateAPIView):
    serializer_class = SaleSerializer

    def get_queryset(self):
        queryset = Sale.objects.all()
        if self.request.company:
            queryset = queryset.filter(company=self.request.company)
        queryset = queryset.filter(party_id=self.kwargs.get('party_pk'))
        receipt_pk = int(self.kwargs.get('receipt_pk'))
        if receipt_pk:
            queryset = queryset.filter(receipts__cash_receipt_id=receipt_pk)
        else:
            queryset = queryset.filter(pending_amount__gt=0)
        return queryset


class PendingPurchaseListAPI(generics.ListCreateAPIView):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        queryset = Purchase.objects.all()
        if self.request.company:
            queryset = queryset.filter(company=self.request.company)
        queryset = queryset.filter(party_id=self.kwargs.get('party_pk'))
        payment_pk = int(self.kwargs.get('payment_pk'))
        if payment_pk:
            queryset = queryset.filter(receipts__cash_payment_id=payment_pk)
        else:
            queryset = queryset.filter(pending_amount__gt=0)
        return queryset
