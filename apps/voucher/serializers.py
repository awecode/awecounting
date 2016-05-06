from rest_framework import serializers
from .models import FixedAsset, FixedAssetRow, AdditionalDetail, CashPayment, CashPaymentRow, CashReceipt, CashReceiptRow, PurchaseVoucherRow, PurchaseVoucher, SaleRow, Sale, JournalVoucherRow, JournalVoucher, \
PurchaseOrder, PurchaseOrderRow, ExpenseRow, Expense


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


class PurchaseVoucherRowSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField(source='item.id')
    unit_id = serializers.ReadOnlyField(source='unit.id')

    class Meta:
        model = PurchaseVoucherRow
        exclude = ['item', 'unit']


class PurchaseVoucherSerializer(serializers.ModelSerializer):
    rows = PurchaseVoucherRowSerializer(many=True)
    date = serializers.DateField(format=None)
    party_id = serializers.ReadOnlyField()

    class Meta:
        model = PurchaseVoucher
        exclude = ['party']


class PurchaseOrderRowSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField(source='item.id')
    unit_id = serializers.ReadOnlyField(source='unit.id')

    class Meta:
        model = PurchaseOrderRow
        exclude = ['item', 'unit']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    rows = PurchaseOrderRowSerializer(many=True)
    date = serializers.DateField(format=None)
    party_id = serializers.ReadOnlyField()

    class Meta:
        model = PurchaseOrder
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


class AdditionalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalDetail


class FixedAssetRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedAssetRow


class FixedAssetSerializer(serializers.ModelSerializer):
    rows = FixedAssetRowSerializer(many=True)
    additional_details = AdditionalDetailSerializer(many=True)

    class Meta:
        model = FixedAsset


class ExpenseRowSerializer(serializers.ModelSerializer):
    expense_id = serializers.ReadOnlyField(source='expense.id')
    pay_head_id = serializers.ReadOnlyField(source='pay_head.id')

    class Meta:
        model = ExpenseRow


class ExpenseSerializer(serializers.ModelSerializer):
    rows = ExpenseRowSerializer(many=True)

    class Meta:
        model = Expense