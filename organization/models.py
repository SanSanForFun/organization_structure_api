from django.db import models


class Department(models.Model):
    """ Модель подразделение """
    name = models.CharField(unique=True, null=False, max_length=200, verbose_name='Название подразделения')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children',
                               verbose_name='Родительское подразделение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Employee(models.Model):
    """ Модель сотрудник """
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees',
                                      verbose_name='Подразделение')
    full_name = models.CharField(max_length=200, null=False, verbose_name='ФИО')
    position = models.CharField(max_length=200, null=False, verbose_name='Должность')
    hired_at = models.DateField(null=True, blank=True, verbose_name='Дата приема')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name
