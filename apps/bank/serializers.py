from rest_framework import serializers
from apps.bank.models import ChequeDeposit, ChequeDepositRow, File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File


class ChequeDepositRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequeDepositRow


class ChequeDepositSerializer(serializers.ModelSerializer):
    rows = ChequeDepositRowSerializer(many=True)
    file = FileSerializer(many=True)

    class Meta:
        model = ChequeDeposit
