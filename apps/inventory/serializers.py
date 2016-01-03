from rest_framework import serializers

from .models import Item, Unit, JournalEntry, UnitConverter


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit


class ItemSerializer(serializers.ModelSerializer):
    unit = UnitSerializer()
    name = serializers.ReadOnlyField(source='__unicode__')
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.name

    class Meta:
        model = Item
        # exclude = ['unit']


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
                unit_converter = UnitConverter.objects.get(base_unit__name=default_unit,
                                                           unit_to_convert__name=obj.creator.unit.name)
                multiple = unit_converter.multiple
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
                unit_converter = UnitConverter.objects.get(base_unit__name=default_unit,
                                                           unit_to_convert__name=obj.creator.unit.name)
                multiple = unit_converter.multiple
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
        if obj.creator.__class__.__name__ == 'PurchaseRow':
            return ''
        else:
            default_unit = self.context.get('default_unit')
            if obj.creator.unit.name != default_unit:
                unit_converter = UnitConverter.objects.get(base_unit__name=default_unit,
                                                           unit_to_convert__name=obj.creator.unit.name)
                multiple = unit_converter.multiple
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
        if obj.creator.__class__.__name__ == 'PurchaseRow':
            return ''
        return obj.creator.rate

    def get_current_balance(self, obj):
        return obj.transactions.filter(account=obj.creator.item.account)[0].current_balance
