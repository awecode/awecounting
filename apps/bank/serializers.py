from rest_framework import serializers
from apps.bank.models import ChequeDeposit, ChequeDepositRow
from awecounting.utils.mixins import SerializerWithFile


class ChequeDepositRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequeDepositRow


class ChequeDepositSerializer(SerializerWithFile, serializers.ModelSerializer):
    rows = ChequeDepositRowSerializer(many=True)
    files = serializers.SerializerMethodField()

    class Meta:
        model = ChequeDeposit
