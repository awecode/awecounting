from rest_framework import serializers
from bank.models import ChequeDeposit, ChequeDepositRow, ChequePayment, ElectronicFundTransferIn, ElectronicFundTransferInRow, ElectronicFundTransferOut


class ChequeDepositRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequeDepositRow


class ChequeDepositSerializer(serializers.ModelSerializer):
    rows = ChequeDepositRowSerializer()

    class Meta:
        model = ChequeDeposit


class ChequePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequePayment


class ElectronicFundTransferOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronicFundTransferOut

class ElectronicFundTransferInRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronicFundTransferInRow


class ElectronicFundTransferInSerializer(serializers.ModelSerializer):
    rows = ElectronicFundTransferInRowSerializer()

    class Meta:
        model = ElectronicFundTransferIn