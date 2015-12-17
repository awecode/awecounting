from rest_framework import serializers
from apps.account.models import JournalVoucher, JournalVoucherRow


class JournalVoucherRowSerializer(serializers.ModelSerializer):
	class Meta:
		model = JournalVoucherRow


class JournalVoucherSerializer(serializers.ModelSerializer):
	rows = JournalVoucherRowSerializer(many=True)

	class Meta:
		model = JournalVoucher