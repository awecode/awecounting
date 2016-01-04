from rest_framework import serializers
from .models import Account, Party


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
