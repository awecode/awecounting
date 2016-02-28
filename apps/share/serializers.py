from rest_framework import serializers
from apps.share.models import ShareHolder, Collection, Investment


class ShareHolderSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = ShareHolder


class CollectionSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Collection


class InvestmentSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Investment