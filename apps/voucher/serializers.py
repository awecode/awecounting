from rest_framework import serializers
from ..voucher.models import CashReceipt, CashReceiptRow


class CashReceiptRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashReceiptRow


class CashReceiptSerializer(serializers.ModelSerializer):
    rows = CashReceiptRowSerializer(many=True)

    class Meta:
        model = CashReceipt
