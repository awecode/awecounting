from rest_framework import serializers
from apps.payroll.models import Entry, EntryRow, Employee


class EntryRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryRow


class EntrySerializer(serializers.ModelSerializer):
    rows = EntryRowSerializer(many=True)

    class Meta:
        model = Entry


class EmployeeSerializer(serializers.ModelSerializer):
    unpaid_days = serializers.ReadOnlyField(source='get_unpaid_days')
    unpaid_hours = serializers.ReadOnlyField(source='get_unpaid_hours')
    unpaid_ot_hours = serializers.ReadOnlyField(source='get_unpaid_ot_hours')

    class Meta:
        model = Employee
        fields = ['name', 'id', 'tax_id', 'unpaid_days', 'unpaid_hours', 'unpaid_ot_hours']
