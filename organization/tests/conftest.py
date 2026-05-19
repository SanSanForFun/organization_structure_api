import pytest
from rest_framework.test import APIClient
from organization.models import Department, Employee


@pytest.fixture
def api_client():
    """Базовый клиент DRF для тестов API"""
    return APIClient()


@pytest.fixture
def root_dept(db):
    """Корневое подразделение (без родителя)"""
    return Department.objects.create(name="Головной офис")


@pytest.fixture
def child_dept(db, root_dept):
    """Дочернее подразделение"""
    return Department.objects.create(name="Backend-отдел", parent=root_dept)


@pytest.fixture
def employee(db, child_dept):
    """Сотрудник в дочернем подразделении"""
    return Employee.objects.create(
        full_name="Мочалкин Петр Ильич",
        position="Backend Developer",
        department_id=child_dept
    )
