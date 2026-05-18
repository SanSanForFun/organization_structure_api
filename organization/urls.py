from django.urls import path

from organization.views import EmployeeCreateAPIView, DepartmentCreateAPIView, DepartmentRetrieveAPIView, DepartmentUpdateAPIView, DepartmentDestroyAPIView

urlpatterns = [
    path('departments/<int:id>/employees/', EmployeeCreateAPIView.as_view(), name='employee-create'),
    path('departments/create', DepartmentCreateAPIView.as_view(), name='dept-create'),
    path('departments/<int:id>/', DepartmentRetrieveAPIView.as_view(), name='dept-detail'),
    path('departments/<int:id>/update', DepartmentUpdateAPIView.as_view(), name='dept-update'),
    path('departments/<int:id>/delete', DepartmentDestroyAPIView.as_view(), name='dept-delete'),
]
