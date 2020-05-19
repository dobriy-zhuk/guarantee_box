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

    amount: account balance, how much money does the student have
    currency: RUB, USD or EUR

    Arguments:
        models.Model: superclass which describes fields for database
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    age = models.PositiveSmallIntegerField(default=0)
    phone = models.TextField(max_length=500, blank=True, default='712312')
    city = models.CharField(max_length=60, default='')
    amount = models.IntegerField(default=0)
    status = models.ForeignKey(
        StudentStatus, default=1, on_delete=models.CASCADE
    )
    currency = models.CharField(max_length=3, default='RUB')
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        """Override the str() behavior, for instance of class.

        Returns:
            self.title: Instance title
        """
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.TextField(max_length=500, blank=True, default='79151761287')
    city = models.CharField(max_length=60, default='')
    status = models.ForeignKey(
        TeacherStatus, default=1, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class TeacherSchedule(models.Model):
    """Class describe teacher scheduler.

    start_timestamp: начальная отметка времени, когда преподаватель занят
    end_timestamp: конечная отметка времени, когда преподаватель занят

    theory:
        timedelta = datetime.timedelta(minumanage.py migrate --faketes=45)
        
        what can be transferred to timedelta:
        class datetime.timedelta(
            days=0, seconds=0, microseconds=0,
            milliseconds=0, minutes=0, hours=0, weeks=0

    example:
        end_timestamp = start_timestamp + datetime.timedelta(minutes=45)

    Arguments:
        models.Model: superclass which describes fields for database
    """

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=200)
    student_name = models.CharField(max_length=200)
    phone = models.TextField(max_length=500, blank=True, default='79151761287')
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()
