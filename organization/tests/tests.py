import pytest
from organization.models import Department, Employee

pytestmark = pytest.mark.django_db

BASE_DEPT = "/organization/departments/"


class TestDepartmentCRUD:
    """Тесты создания и получения подразделений"""

    def test_create_department(self, api_client):
        response = api_client.post(f"{BASE_DEPT}create", {"name": "Новый отдел"}, format="json")
        assert response.status_code == 201
        assert Department.objects.filter(name="Новый отдел").exists()

    def test_retrieve_department_with_tree(self, api_client, child_dept, employee):
        response = api_client.get(f"{BASE_DEPT}{child_dept.id}/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Backend-отдел"
        assert len(data["employees"]) == 1
        assert data["employees"][0]["full_name"] == "Мочалкин Петр Ильич"
        assert data["children"] == []

    def test_patch_department_move(self, api_client, child_dept):
        new_parent = Department.objects.create(name="Финансы")
        response = api_client.patch(
            f"{BASE_DEPT}{child_dept.id}/update",
            {"parent_id": new_parent.id},
            format="json"
        )
        assert response.status_code == 200
        child_dept.refresh_from_db()
        assert child_dept.parent_id == new_parent.id


class TestDepartmentValidation:
    """Тесты бизнес-валидации дерева"""

    def test_self_parent_forbidden(self, api_client, root_dept):
        response = api_client.patch(
            f"{BASE_DEPT}{root_dept.id}/update",
            {"parent_id": root_dept.id},
            format="json"
        )
        assert response.status_code == 400
        assert "родителем самого себя" in response.json()["parent_id"][0]

    def test_cycle_forbidden(self, api_client, root_dept, child_dept):
        response = api_client.patch(
            f"{BASE_DEPT}{root_dept.id}/update",
            {"parent_id": child_dept.id},
            format="json"
        )
        assert response.status_code == 400
        assert "цикл" in response.json()["parent_id"][0].lower()


class TestEmployeeCreation:
    """Тесты создания сотрудников"""

    def test_create_employee_success(self, api_client, child_dept):
        url = f"{BASE_DEPT}{child_dept.id}/employees/"
        data = {"full_name": "Веников Вениамин Поликарпович", "position": "QA"}
        response = api_client.post(url, data, format="json")

        assert response.status_code == 201
        emp = Employee.objects.get(full_name="Веников Вениамин Поликарпович")
        assert emp.department_id == child_dept

    def test_create_employee_invalid_department(self, api_client, child_dept):
        url = f"{BASE_DEPT}{child_dept.id}/employees/"
        data = {"full_name": "Ошибка", "position": "Dev", "department_id": 9999}
        response = api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert "department_id" in response.json()


class TestDepartmentDeletion:
    """Тесты удаления подразделений (cascade / reassign)"""

    def test_delete_cascade(self, api_client):
        root = Department.objects.create(name="Root")
        child = Department.objects.create(name="Child", parent=root)
        emp = Employee.objects.create(
            full_name="Emp", position="Dev", department_id=child
        )

        response = api_client.delete(f"{BASE_DEPT}{root.id}/delete?mode=cascade")

        assert response.status_code == 204
        assert not Department.objects.filter(id=root.id).exists()
        assert not Department.objects.filter(id=child.id).exists()
        assert not Employee.objects.filter(id=emp.id).exists()

    def test_delete_reassign(self, api_client):
        target = Department.objects.create(name="Target")
        source = Department.objects.create(name="Source")
        emp = Employee.objects.create(
            full_name="Emp", position="Dev", department_id=source
        )

        response = api_client.delete(
            f"{BASE_DEPT}{source.id}/delete?mode=reassign&reassign_to_department_id={target.id}"
        )

        assert response.status_code == 204
        emp.refresh_from_db()
        assert emp.department_id == target
        assert not Department.objects.filter(id=source.id).exists()
