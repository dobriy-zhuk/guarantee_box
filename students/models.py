from django.db import models
from django.contrib.auth.models import User


class StudentStatus(models.Model):
    name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class TeacherStatus(models.Model):
    name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.TextField(max_length=500, blank=True, default='712312')
    city = models.CharField(max_length=60, default='')
    amount = models.IntegerField(default=0)
    status = models.ForeignKey(StudentStatus, default=1, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, default='RUB')

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.TextField(max_length=500, blank=True, default='79151761287')
    city = models.CharField(max_length=60, default='')
    status = models.ForeignKey(TeacherStatus, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


