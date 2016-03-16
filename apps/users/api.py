from rest_framework import viewsets
from rest_framework import generics
from .serializers import UserSerializer, GroupSerializer, CompanySerializer
from .models import User, Pin, Company
from django.contrib.auth.models import Group

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class AccessibleCompanyAPI(generics.ListAPIView):
	serializer_class = CompanySerializer

	def get_queryset(self):
		return Pin.accessible_companies(self.request.company)
