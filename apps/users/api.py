from django.contrib.auth.models import Group

from rest_framework import viewsets
from rest_framework import generics
from .serializers import UserSerializer, GroupSerializer, CompanySerializer
from .models import User, Pin


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


# class SetPagination(pagination.PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 1000


class AccessibleCompanyAPI(generics.ListAPIView):
    serializer_class = CompanySerializer
    # pagination_class = SetPagination

    def get_queryset(self):
        qs = []
        if self.request.company:
            qs =  Pin.accessible_companies(self.request.company)
        return qs



class UserListAPI(generics.ListAPIView):
    serializer_class = UserSerializer
    # pagination_class = SetPagination

    def get_queryset(self):
        queryset = User.objects.all()
        if 'group' in self.request.GET:
            queryset = queryset.filter(groups__name=self.request.GET.get('group'))
        return queryset
