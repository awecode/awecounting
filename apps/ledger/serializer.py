from rest_framework import serializers
from .models import Account, JournalVoucher, JournalVoucherRow


class JournalVoucherRowSerializer(serializers.ModelSerializer):
	class Meta:
		model = JournalVoucherRow


class JournalVoucherSerializer(serializers.ModelSerializer):
	rows = JournalVoucherRowSerializer(many=True)

	class Meta:
		model = JournalVoucher

		
class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
