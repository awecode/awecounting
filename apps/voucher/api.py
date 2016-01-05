from rest_framework import generics
from .serializers import SaleSerializer
from .models import Sale, CashReceipt


class PendingSaleListAPI(generics.ListCreateAPIView):
    # queryset = Sale.objects.all()
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
