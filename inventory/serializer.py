from rest_framework import serializers
from inventory.models import Purchase, PurchaseRow, Item, Party, Unit, Sale, SaleRow, JournalEntry, none_for_zero, zero_for_none

class ItemSerializer(serializers.ModelSerializer):
	unit_id = serializers.ReadOnlyField(source='unit.id')

	class Meta:
		model = Item
		exclude = ['unit']

class UnitSerializer(serializers.ModelSerializer):

	class Meta:
		model = Unit

class PartySerializer(serializers.ModelSerializer):

	class Meta:
		model = Party

class PurchaseRowSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField(source='item.id')
    unit_id = serializers.ReadOnlyField(source='unit.id')

    class Meta:
        model = PurchaseRow
        exclude = ['item', 'unit']
        
class PurchaseSerializer(serializers.ModelSerializer):
    rows = PurchaseRowSerializer(many=True)
    date = serializers.DateField(format=None)

    class Meta:
        model = Purchase
        # exclude = ['date']

class SaleRowSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField(source='item.id')
    unit_id = serializers.ReadOnlyField(source='unit.id')

    class Meta:
        model = SaleRow
        exclude = ['item', 'unit']
        
class SaleSerializer(serializers.ModelSerializer):
    rows = SaleRowSerializer(many=True)
    date = serializers.DateField(format=None)

    class Meta:
        model = Sale

class InventoryAccountRowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    # voucher_no = serializers.ReadOnlyField()
    # specification = serializers.ReadOnlyField(source='creator.specification')
    # country_or_company = serializers.SerializerMethodField()
    # size = serializers.SerializerMethodField()
    # expected_life = serializers.SerializerMethodField()
    # source = serializers.SerializerMethodField()
    income_quantity = serializers.SerializerMethodField()
    income_rate = serializers.SerializerMethodField()
    # income_total = serializers.SerializerMethodField()
    expense_quantity = serializers.SerializerMethodField()
    expense_rate = serializers.SerializerMethodField()
    # expense_total_cost_price = serializers.SerializerMethodField()
    # remaining_total_cost_price = serializers.SerializerMethodField()
    # remarks = serializers.SerializerMethodField()
    current_balance = serializers.SerializerMethodField()
    date = serializers.DateField(format=None)

    class Meta:
        model = JournalEntry

    # def get_voucher_no(self, obj):
        # if obj.creator.__class__ == SaleRow:
        #     return zero_for_none(obj.creator.sale.voucher_no)
        # elif obj.creator.__class__ == PurchaseRow:
        #     return zero_for_none(obj.creator.purchase.voucher_no)

    # def get_country_or_company(self, obj):
    #     try:
    #         return obj.account_row.country_of_production_or_company_name
    #     except:
    #         return ''

    # def get_size(self, obj):
    #     try:
    #         return obj.account_row.size
    #     except:
    #         return ''

    # def get_expected_life(self, obj):
    #     try:
    #         return obj.account_row.expected_life
    #     except:
    #         return ''

    # def get_source(self, obj):
    #     try:
    #         return obj.account_row.source
    #     except:
    #         return ''

    def get_income_quantity(self, obj):
        if obj.creator.__class__ == SaleRow:
            return ''
        return obj.creator.quantity

    def get_income_rate(self, obj):
        if obj.creator.__class__ == SaleRow:
            return ''
        return obj.creator.rate

    # def get_income_total(self, obj):
    #     if obj.creator.__class__ == DemandRow:
    #         return ''
    #     import math

    #     return math.ceil(obj.creator.total_entry_cost() * 100) / 100

    def get_expense_quantity(self, obj):
        if obj.creator.__class__ == PurchaseRow:
            return ''
        return obj.creator.quantity

    def get_expense_rate(self, obj):
        if obj.creator.__class__ == PurchaseRow:
            return ''
        return obj.creator.rate

    # def get_expense_total_cost_price(self, obj):
    #     try:
    #         return obj.account_row.expense_total_cost_price or ''
    #     except:
    #         return ''

    # def get_remaining_total_cost_price(self, obj):
    #     try:
    #         return obj.account_row.remaining_total_cost_price or ''
    #     except:
    #         return ''


    # def get_remarks(self, obj):
    #     try:
    #         return obj.account_row.remarks
    #     except:
    #         return ''

    def get_current_balance(self, obj):
        return obj.transactions.filter(account=obj.creator.item.account)[0].current_balance


