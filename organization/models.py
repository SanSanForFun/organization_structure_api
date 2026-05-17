from django.db import models


class Department(models.Model):
    """ Модель подразделение """
    id = models.IntegerField(unique=True, verbose_name='id')
    name = models.CharField(unique=True, null=False, max_length=200, verbose_name='Название подразделения')
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    """ Модель сотрудник """
    id = models.IntegerField(unique=True, verbose_name='id')
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=False)
    position = models.CharField(max_length=200, null=False)
    hired_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name