from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from managers.models import Manager
from datetime import date


class StudentStatus(models.Model):
    """Describe status for Student.

    Note: Student can be 'lead' or 'full student'
    'lead' is student before enroll
    'full student' is student after enroll

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

    currency: RUB, USD or EUR

    amount: account balance, how much money does the student have
    Max number is 99999.99

    Student phone is writed in comment

    communication : calls what manager has did to student

    """

    class StudentLevel(models.TextChoices):
        BEGINNER = 'BG', _('Beginner')
        MIDDLE = 'MD', _('Middle')
        ADVANCED = 'AD', _('Advanced')

    class StudentSource(models.TextChoices):
        FACEBOOK = 'FB', _('Facebook')
        VKONTAKTE = 'VK', _('Vkontakte')
        INSTAGRAM = 'IN', _('Instagram')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200) 
    parent_name = models.CharField(max_length=200, default='')
    phone = models.TextField(
        max_length=500, blank=True, default='7123123',
    )
    parent_phone = models.TextField(
        max_length=500, blank=True, default='712312',
    )
    email = models.EmailField(max_length=254, default='')
    parent_email = models.EmailField(max_length=254, default='')
    city = models.CharField(max_length=60, default='')
    amount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    reward_card_amount = models.PositiveIntegerField(default=0)
    status = models.ForeignKey(
        StudentStatus, default=1, on_delete=models.CASCADE
    )
    currency = models.CharField(max_length=3, default='RUB')
    image = models.ImageField(
        blank=True, default='', upload_to='images',
    )
    student_level = models.CharField(
        max_length=2,
        choices=StudentLevel.choices,
        default=StudentLevel.BEGINNER,
    )
    responsible_manager = models.ForeignKey(
        Manager,
        related_name='responsible_students',
        on_delete=models.CASCADE,
    )
    communication = models.CharField(max_length=250, default='')
    subject = models.CharField(max_length=250, default='')
    source = models.CharField(
        max_length=2,
        choices=StudentSource.choices,
        default=StudentSource.FACEBOOK,
    )
    school = models.CharField(max_length=300, default='')
    school_class = models.CharField(max_length=3, default='')
    created_date = models.DateTimeField(auto_now_add=True)
    signup_confirmation = models.BooleanField(default=False)
    birthday = models.DateField(null=True)

    @property
    def age(self):
        today = date.today()
        birthday = self.birthday
        return today.year - birthday.year - (
            (today.month, today.day) < (birthday.month, birthday.day)
        )

    def __str__(self):
        """Override the str() behavior, for instance of class.

        Returns:
            self.name: Instance name
        """
        return self.name


class Teacher(models.Model):
    
    class TeacherCurrency(models.TextChoices):
        RUBLE = 'RUB', _('Ruble')
        DOLLAR = 'USD', _('Dollar')
        EURO = 'EUR', _('Euro')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.TextField(max_length=500, blank=True, default='79151761287')
    email = models.EmailField(max_length=254, default='')
    city = models.CharField(max_length=60, default='')
    status = models.ForeignKey(
        TeacherStatus, default=1, on_delete=models.CASCADE
    )
    students = models.ManyToManyField(
        'Student',
        related_name='teachers',
        blank=True,
    )
    amount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=TeacherCurrency.choices,
        default=TeacherCurrency.RUBLE,
    )
    salary_rate = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2,
    )
    salary_rate_time_interval = models.DurationField(
        blank=True, default=timedelta(minutes=60),
    )
    manager = models.ForeignKey(
        Manager,
        related_name='supervised_teachers',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """Override the str() behavior, for instance of class.

        Returns:
            self.name: Instance name
        """
        return self.name


class Schedule(models.Model):
    """Class describe user scheduler.

    start_timestamp: начальная отметка времени, когда user занят
    end_timestamp: конечная отметка времени, когда user занят

    Когда я создаю пользователя, то, только в связанных таблицах Teacher или 
    Student он указывает свое имя, которео можно подтянуть user.student или
    user.teacher. Если хотите взять узнать телефон, то нужно вызвать
    user.student.phone или user.teacher.phone

    Comment (str): '{0} имя родителя, {1} тел. родителя,
            {2} имя ученика'.format(
                parent_name, parent_phone, student_name,
            )

    Схема Schedule выяглядит таким образом

    User | Comment | Start_timestamp | End_timestamp
    -----+---------+-----------------+--------------
    user1            29.12.2020 12:45  29.12.2020 13:15
    user1            30.12.2020 12:45  30.12.2020 13:15

    user1.teacher = True
    timedelta = user1.end_timestamp - user1.start_timestamp
    timedelta : time when teacher is busy
    
    theory:
        timedelta = datetime.timedelta(minutes=45)
        
        what can be transferred to timedelta:
        class datetime.timedelta(
            days=0, seconds=0, microseconds=0,
            milliseconds=0, minutes=45, hours=0, weeks=0
        )

    example:
        end_timestamp = start_timestamp + datetime.timedelta(minutes=45)

    Arguments:
        models.Model: superclass which describes fields for database
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300, blank=True)
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()

    def __str__(self):
        """Override the str() behavior, for instance of class.

        Returns:
            self.student_name: Instance student_name
        """
        return '{0} schedule'.format(self.user)


class StudentRewardCard(models.Model):
    """Describe students_studentrewardcard table in db.

    Arguments:
        models {[type]} -- [description]
    """

    student = models.ForeignKey(
        Student,
        related_name='reward_cards',
        on_delete=models.CASCADE,    
    )
    lesson_room = models.ForeignKey(
        'courses.LessonRoom',
        related_name='reward_cards',
        on_delete=models.CASCADE,
    )
    teacher = models.ForeignKey(
        Teacher,
        related_name='set_reward_cards',
        on_delete=models.CASCADE,
    )
    comment = models.CharField(max_length=200, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        """Override the str() behavior, for instance of class.

        Returns:
            self.student: Instance student
        """
        return '{0} reward card'.format(self.student)
