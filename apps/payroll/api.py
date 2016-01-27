from rest_framework import generics
from .models import Employee
from .serializers import EmployeeSerializer
from awecounting.utils.mixins import CompanyAPI


class EmployeeListAPI(CompanyAPI, generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer

