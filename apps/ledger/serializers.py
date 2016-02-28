from rest_framework import serializers
from .models import Account, Party, Category


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party


class PartyBalanceSerializer(serializers.ModelSerializer):
    current_cr = serializers.ReadOnlyField(source='account.current_cr')
    current_dr = serializers.ReadOnlyField(source='account.current_dr')
    balance = serializers.ReadOnlyField(source='account.balance')

    class Meta:
        model = Party


class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
