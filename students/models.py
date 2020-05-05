from django.db import models
from django.contrib.auth.models import User


class StudentStatus(models.Model):
    """Describe status for Student.

    Note: Student can be 'lead' or 'full stundet'
    'lead' is student before enroll
    'full student' is student after enroll

    Arguments:
        models.Model: superclass which describes fields
        for database
    """
    name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class TeacherStatus(models.Model):
    name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class Student(models.Model):
    """Describe students_student table in database.

    Arguments:
        models.Model: superclass which describes fields for database
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    age = models.PositiveSmallIntegerField(default=0)
    phone = models.TextField(max_length=500, blank=True, default='712312')
    city = models.CharField(max_length=60, default='')
    amount = models.IntegerField(default=0)
    status = models.ForeignKey(StudentStatus, default=1, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, default='RUB')
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        """Override the str() behavior, for instance of class.

        Returns:
            self.title: Instance title
        """
        return self.name


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.TextField(max_length=500, blank=True, default='79151761287')
    city = models.CharField(max_length=60, default='')
    status = models.ForeignKey(TeacherStatus, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


