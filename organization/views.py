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

    @swagger_auto_schema(
        operation_description="Удалить подразделение",
        manual_parameters=[
            openapi.Parameter(
                name='mode',
                in_=openapi.IN_QUERY,
                description="Режим удаления: cascade (полное удаление) или reassign (перевод сотрудников)",
                type=openapi.TYPE_STRING,
                required=True,
                enum=['cascade', 'reassign']
            ),
            openapi.Parameter(
                name='reassign_to_department_id',
                in_=openapi.IN_QUERY,
                description="ID подразделения для перевода сотрудников (обязателен при mode=reassign)",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={
            204: 'Подразделение успешно удалено',
            400: 'Ошибка валидации параметров',
            404: 'Подразделение не найдено'
        }
    )
    def delete(self, request, *args, **kwargs):
        mode = request.query_params.get('mode')
        if mode not in ('cascade', 'reassign'):
            return Response(
                {'detail': 'Укажите mode=cascade или mode=reassign'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reassign_id = request.query_params.get('reassign_to_department_id')
        if mode == 'reassign' and not reassign_id:
            return Response(
                {'detail': 'При mode=reassign обязателен reassign_to_department_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        dept = self.get_object()

        with transaction.atomic():
            if mode == 'reassign':
                try:
                    target = Department.objects.get(pk=reassign_id)
                except Department.DoesNotExist:
                    return Response(
                        {'detail': 'Целевое подразделение не найдено'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Переводим сотрудников
                Employee.objects.filter(department=dept).update(department=target)
                # Удаляем дочерние отделы
                dept.children.all().delete()

            dept.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
