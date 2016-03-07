from rest_framework import serializers
from .models import Account, Party, Category
from ..tax.serializers import PartyTaxPreferenceSerializer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account


class PartySerializer(serializers.ModelSerializer):
    tax_preference = PartyTaxPreferenceSerializer()

    class Meta:
        model = Party


class PartyBalanceSerializer(serializers.ModelSerializer):
    current_cr = serializers.ReadOnlyField(source='account.current_cr')
    current_dr = serializers.ReadOnlyField(source='account.current_dr')
    balance = serializers.ReadOnlyField(source='account.balance')
    tax_preference = PartyTaxPreferenceSerializer()

    class Meta:
        model = Party


class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
