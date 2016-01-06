from rest_framework import serializers
from .models import CashPayment, CashPaymentRow, CashReceipt, CashReceiptRow, PurchaseRow, Purchase, SaleRow, Sale, JournalVoucherRow, JournalVoucher


class CashReceiptRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashReceiptRow


class CashReceiptSerializer(serializers.ModelSerializer):
    rows = CashReceiptRowSerializer(many=True)
    party_id = serializers.ReadOnlyField()

    class Meta:
        model = CashReceipt
        exclude = ['party']


class CashPaymentRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashPaymentRow


class CashPaymentSerializer(serializers.ModelSerializer):
    rows = CashPaymentRowSerializer(many=True)
    party_id = serializers.ReadOnlyField()

    class Meta:
        model = CashPayment
        exclude = ['party']


class PurchaseRowSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField(source='item.id')
    unit_id = serializers.ReadOnlyField(source='unit.id')

    class Meta:
        model = PurchaseRow
        exclude = ['item', 'unit']


class PurchaseSerializer(serializers.ModelSerializer):
    rows = PurchaseRowSerializer(many=True)
    date = serializers.DateField(format=None)
    party_id = serializers.ReadOnlyField()

    class Meta:
        model = Purchase
        exclude = ['party']


class SaleRowSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField(source='item.id')
    unit_id = serializers.ReadOnlyField(source='unit.id')

    class Meta:
        model = SaleRow
        exclude = ['item', 'unit']


class SaleSerializer(serializers.ModelSerializer):
    rows = SaleRowSerializer(many=True)
    date = serializers.DateField(format=None)
    party_id = serializers.ReadOnlyField()

    class Meta:
        model = Sale
        exclude = ['party']


class JournalVoucherRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalVoucherRow


class JournalVoucherSerializer(serializers.ModelSerializer):
    rows = JournalVoucherRowSerializer(many=True)

    class Meta:
        model = JournalVoucher
