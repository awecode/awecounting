from rest_framework import serializers
from .models import TaxScheme


class TaxSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxScheme
