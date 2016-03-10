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
    class Meta:
        model = Company
