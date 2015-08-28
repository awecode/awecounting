from rest_framework import serializers
from inventory.models import Purchase, PurchaseRow, Item, Party, Unit, Sale, SaleRow

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
