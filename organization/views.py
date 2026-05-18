from organization.models import Department, Employee
from organization.serializers import DepartmentSerializer, EmployeeSerializer, DepartmentDetailSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class EmployeeCreateAPIView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class DepartmentListAPIView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentCreateAPIView(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Department.objects.select_related('parent').prefetch_related('employees', 'children',
                                                                            'children__employees')
    serializer_class = DepartmentDetailSerializer
    lookup_field = 'id'


class DepartmentUpdateAPIView(generics.UpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'id'
    http_method_names = ['patch']


class DepartmentDestroyAPIView(generics.DestroyAPIView):
    queryset = Department.objects.all()
    lookup_field = 'id'
    http_method_names = ['delete']