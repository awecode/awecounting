from rest_framework import serializers

from .models import User, File, Company
from django.contrib.auth.models import Group


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group


class CompanySerializer(serializers.ModelSerializer):
    added_date = serializers.SerializerMethodField()

    class Meta:
        model = Company

    def get_added_date(self, obj):
    	self.request = self.context['request'].company
    	return self.request.used_pin.get(company=obj).date
