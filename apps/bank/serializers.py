from rest_framework import serializers
from apps.bank.models import ChequeDeposit, ChequeDepositRow
from ..users.serializers import FileSerializer


class ChequeDepositRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequeDepositRow


class ChequeDepositSerializer(serializers.ModelSerializer):
    rows = ChequeDepositRowSerializer(many=True)
    files = FileSerializer(many=True)

    class Meta:
        model = ChequeDeposit
