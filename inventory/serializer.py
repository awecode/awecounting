from rest_framework import serializers
from inventory.models import Purchase, PurchaseRow

class PurchaseRowSerializer(serializers.ModelSerializer):
    item_id = serializers.ReadOnlyField(source='item.id')
    unit_id = serializers.ReadOnlyField(source='unit.id')

    class Meta:
        model = PurchaseRow
        exclude = ['item', 'unit']
        
class PurchaseSerializer(serializers.ModelSerializer):
    rows = PurchaseRowSerializer(many=True)

    class Meta:
        model = Purchase
        exclude = ['date']
