from rest_framework import serializers
from apps.payroll.models import Entry, EntryRow


class EntryRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryRow


class EntrySerializer(serializers.ModelSerializer):
    rows = EntryRowSerializer(many=True)

    class Meta:
        model = Entry