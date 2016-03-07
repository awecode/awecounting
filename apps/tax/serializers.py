from rest_framework import serializers
from .models import TaxScheme, PartyTaxPreference


class TaxSchemeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = TaxScheme
        exclude = ('name',)

    def get_name(self, obj):
    	return obj.__str__()


class PartyTaxPreferenceSerializer(serializers.ModelSerializer):
	class Meta:
		model = PartyTaxPreference
