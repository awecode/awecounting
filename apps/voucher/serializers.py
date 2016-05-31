from rest_framework import serializers
from ..users.models import User
from ..users.serializers import UserSerializer
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
    item_id = serializers.ReadOnlyField()
    unit_id = serializers.ReadOnlyField()
    tax_scheme_id = serializers.ReadOnlyField()
    lot_number = serializers.CharField(source='lot.lot_number')

    class Meta:
        model = PurchaseVoucherRow
        exclude = ['item', 'unit', 'tax_scheme', 'lot']


class PurchaseVoucherSerializer(serializers.ModelSerializer):
    rows = PurchaseVoucherRowSerializer(many=True)
    date = serializers.DateField(format=None)
    tax_scheme_id = serializers.ReadOnlyField()
    party_id = serializers.ReadOnlyField()

    class Meta:
        model = PurchaseVoucher
        exclude = ['party', 'tax_scheme']


class PurchaseOrderRowSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField()
    unit_id = serializers.ReadOnlyField()

    class Meta:
        model = PurchaseOrderRow
        exclude = ['item', 'unit']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    rows = PurchaseOrderRowSerializer(many=True)
    date = serializers.DateField(format=None)
    purchase_agent_id = serializers.ReadOnlyField()
    party_id = serializers.ReadOnlyField()
    agents = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        exclude = ['party', 'purchase_agent']

    def get_agents(self, obj):
        users = User.objects.filter(roles__group__name='PurchaseAgent')
        data = []
        for user in users:
            dct = dict(name=user.username, id = user.pk)
            data.append(dct)
        return data


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
        exclude = ('expense', 'pay_head')


class ExpenseSerializer(serializers.ModelSerializer):
    rows = ExpenseRowSerializer(many=True)

    class Meta:
        model = Expense