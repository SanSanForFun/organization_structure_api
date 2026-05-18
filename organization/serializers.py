from rest_framework import serializers
from organization.models import Department, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'position', 'hired_at', 'created_at', ]
        read_only_fields = ('id', 'created_at',)


class DepartmentSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='parent',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Department
        fields = ['id', 'name', 'parent_id', 'created_at', ]
        read_only_fields = ('id', 'created_at',)


class DepartmentDetailSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='parent',
        required=False,
        allow_null=True
    )

    employees = EmployeeSerializer(many=True, read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'name', 'parent_id', 'created_at', 'employees', 'children']
        read_only_fields = ('id', 'created_at',)

    def get_children(self, obj):
        max_depth = self.context.get('max_depth', 3)
        current_depth = self.context.get('depth', 0)

        if current_depth >= max_depth:
            return []

        ctx = {**self.context, 'depth': current_depth + 1}
        return DepartmentDetailSerializer(
            obj.children.all(),
            many=True,
            context=ctx
        ).data
