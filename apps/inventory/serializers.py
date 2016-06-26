from rest_framework import serializers

from models import Item, Unit, JournalEntry, UnitConversion, Location
from ..voucher.models import PurchaseVoucherRow, SaleRow


class UnitSerializer(serializers.ModelSerializer):
    # convertible_units = serializers.SerializerMethodField()

    def get_convertible_units(self, obj):
        return obj.convertibles()

    class Meta:
        model = Unit
        exclude = ('company',)


class ItemSerializer(serializers.ModelSerializer):
    unit = UnitSerializer()
    full_name = serializers.SerializerMethodField()
    # current_balance = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(ItemSerializer, self).__init__(*args, **kwargs)
        if self.context.get('request').company.settings.purchase_suggest_by_item and not self.context.get(
                'request').company.settings.purchase_suggest_by_party_item and kwargs.get('context').get(
            'voucher') == 'purchase':
            self.fields['last_purchase_price'] = serializers.SerializerMethodField()
        if self.context.get('request').company.settings.sale_suggest_by_item and not self.context.get(
                'request').company.settings.sale_suggest_by_party_item and kwargs.get('context').get('voucher') == 'sale':
            self.fields['last_sale_price'] = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.name

    def get_current_balance(self, obj):
        if obj.account and obj.account.account_transaction.filter(account=obj.account):
            return obj.account.account_transaction.filter(account=obj.account).last().current_balance
        else:
            return 0

    def get_last_purchase_price(self, obj):
        last_purchase = PurchaseVoucherRow.objects.filter(item=obj,
                                                          purchase__company=self.context.get('request').company).order_by(
            'purchase__date').last()
        return last_purchase.rate if last_purchase else None

    def get_last_sale_price(self, obj):
        last_sale = SaleRow.objects.filter(item=obj, sale__company=self.context.get('request').company).order_by(
            'sale__date').last()
        return last_sale.rate if last_sale else None

    class Meta:
        model = Item
        exclude = ('category', 'account', 'ledger', 'purchase_ledger', 'sale_ledger')


class InventoryAccountRowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    voucher_no = serializers.ReadOnlyField(source='creator.get_voucher_no')
    income_quantity = serializers.SerializerMethodField()
    income_rate = serializers.SerializerMethodField()
    expense_quantity = serializers.SerializerMethodField()
    current_balance = serializers.SerializerMethodField()
    date = serializers.DateField(format=None)

    class Meta:
        model = JournalEntry

    def get_income_quantity(self, obj):
        if obj.creator.__class__.__name__ == 'SaleRow':
            return ''
        else:
            default_unit = self.context.get('default_unit')
            if obj.creator.unit.name != default_unit:
                unit_conversion = UnitConversion.objects.get(base_unit__name=default_unit,
                                                             unit_to_convert__name=obj.creator.unit.name)
                multiple = unit_conversion.multiple
                if self.context.get('unit_multiple'):
                    unit_multiple = self.context.get('unit_multiple')
                    return (obj.creator.quantity * multiple) / unit_multiple
                else:
                    return obj.creator.quantity * multiple
            else:
                if self.context.get('unit_multiple'):
                    unit_multiple = self.context.get('unit_multiple')
                    return obj.creator.quantity / unit_multiple
                else:
                    return obj.creator.quantity

    def get_income_rate(self, obj):
        if obj.creator.__class__.__name__ == 'SaleRow':
            return ''
        else:
            default_unit = self.context.get('default_unit')
            if obj.creator.unit.name != default_unit:
                unit_conversion = UnitConversion.objects.get(base_unit__name=default_unit,
                                                             unit_to_convert__name=obj.creator.unit.name)
                multiple = unit_conversion.multiple
                if self.context.get('unit_multiple'):
                    unit_multiple = self.context.get('unit_multiple')
                    return (obj.creator.rate * unit_multiple) / multiple
                else:
                    return obj.creator.rate / multiple
            else:
                if self.context.get('unit_multiple'):
                    unit_multiple = self.context.get('unit_multiple')
                    return obj.creator.rate * unit_multiple
                else:
                    return obj.creator.rate

    def get_expense_quantity(self, obj):
        if obj.creator.__class__.__name__ == 'PurchaseVoucherRow':
            return ''
        else:
            default_unit = self.context.get('default_unit')
            if obj.creator.unit.name != default_unit:
                unit_conversion = UnitConversion.objects.get(base_unit__name=default_unit,
                                                             unit_to_convert__name=obj.creator.unit.name)
                multiple = unit_conversion.multiple
                if self.context.get('unit_multiple'):
                    unit_multiple = self.context.get('unit_multiple')
                    return (obj.creator.quantity * multiple) / unit_multiple
                else:
                    return obj.creator.quantity * multiple
            else:
                if self.context.get('unit_multiple'):
                    unit_multiple = self.context.get('unit_multiple')
                    return obj.creator.quantity / unit_multiple
                else:
                    return obj.creator.quantity

    def get_expense_rate(self, obj):
        if obj.creator.__class__.__name__ == 'PurchaseVoucherRow':
            return ''
        return obj.creator.rate

    def get_current_balance(self, obj):
        return obj.transactions.filter(account=obj.creator.item.account)[0].current_balance


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'id',
            'name',
            'enabled',
            'parent'
        )
