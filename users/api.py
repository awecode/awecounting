from rest_framework import viewsets

from .serializers import UserSerializer, GroupSerializer
from .models import User
from django.contrib.auth.models import Group

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
