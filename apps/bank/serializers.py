from rest_framework import serializers
from apps.bank.models import ChequeDeposit, ChequeDepositRow, BankAccount, BankCashDeposit, ChequePayment
from awecounting.utils.mixins import SerializerWithFile


class ChequeDepositRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequeDepositRow


class ChequeDepositSerializer(SerializerWithFile, serializers.ModelSerializer):
    rows = ChequeDepositRowSerializer(many=True)
    files = serializers.SerializerMethodField()

    class Meta:
        model = ChequeDeposit


class BankAccountSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = BankAccount


class BankCashDepositSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = BankCashDeposit


class ChequePaymentSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = ChequePayment