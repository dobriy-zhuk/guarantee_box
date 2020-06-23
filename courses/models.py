"""File with classes which describe tables in database."""
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from opentok import OpenTok

from courses.fields import OrderField
from students.models import Schedule, Student, Teacher


class Subject(models.Model):
    """Describe the courses_subject table in database.

    Subject is the theme of lesson.

    Arguments:
        models.Model: superclass where describe the fields
    """
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=200, unique=True)

    class Meta:
        """Metadata class.

        When Django make Subject class, Meta override the ordering.
        """
        ordering = ['title']

    def __str__(self):
        """Override the str() behavior, for instance of class.

        Returns:
            self.title: Instance title
        """
        return self.title


class Course(models.Model):
    """Class describes courses_course table in db.

    cost:
    max value is 99999.99

    repetition can store '1 time a week', '1 time a months', etc.

    """

    class CourseDifficultyLevel(models.TextChoices):
        BEGINNER = 'BG', _('Beginner')
        MIDDLE = 'MD', _('Middle')
        ADVANCED = 'AD', _('Advanced')

    class CourseParticipantLevel(models.TextChoices):
        STUDENT = 'ST', _('Student')
        TEACHER = 'TC', _('Teacher')
        MANAGER = 'MN', _('Manager')

    owner = models.ForeignKey(
        Teacher,
        related_name='courses_created',
        on_delete=models.CASCADE,
    )
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE,
    )
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(
        Student,
        related_name='courses_joined',
        blank=True,
    )
    icon = models.ImageField(blank=True, default='')
    cost = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    old_cost = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2,
    )
    video_url = models.URLField(blank=True, default='')
    image = models.ImageField(blank=True, default='', upload_to='images')
    comment = models.TextField(blank=True, default='')
    testimonial = models.TextField(blank=True, default='')
    testimonial_author = models.TextField(blank=True, default='')
    repetition = models.CharField(max_length=200, blank=True, default='')
    min_participant_age = models.PositiveIntegerField(default=0)
    difficulty_level = models.CharField(
        max_length=2,
        choices=CourseDifficultyLevel.choices,
        default=CourseDifficultyLevel.BEGINNER,
    )
    participant_level = models.CharField(
        max_length=2,
        choices=CourseParticipantLevel.choices,
        default=CourseParticipantLevel.STUDENT,
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    """Describe courses_module table in db.

    Note: чтобы проставить атрибут 'module_done',
    если пользователь закончил курс
    можно прописать:

        class Meta:
            permissions = (
                ('module_done', 'Module done')
            )

    и отдельно для каждого пользователя можно делать:

        from guardian.shortcuts import assign_perm
        assign_perm('module_done', student.user, module)

        student.user.has_perm('module_done', module)
        True
    
    Это значит для конкретного 'student' и 'module'
    значение 'module_done' будет свое

    чтобы удалить атрибут:

        from guardian.shortcuts import remove_perm
        remove_perm('module_done', student.user, module)

        student.user.has_perm('module_done', module)
        False

    How to get QuerySet of student.user permissions:

        from guardians.shortcuts import get_objects_for_user

        student.user.has_perm('module_done')
        False
        
        You need to specify the instanse for permission
        student.user.has_perm('module_done', module)
        True

        get_objects_for_user(student.user, 'courses.module_done')
                                              ^
                                    name of app required
        <QuerySet [<Module: 0. Переменные>]>
    """

    class Meta:
        ordering = ['order']
        permissions = (
            ('view_current_module', 'Can view current module'),
            ('module_done', 'Module done')
        )

    course = models.ForeignKey(
        'Course',
        related_name='modules',
        on_delete=models.CASCADE,
    )
    title = models.CharField(_('title'), max_length=250)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return '{0}. {1}'.format(self.order, self.title)


class Content(models.Model):
    class Meta:
        ordering = ['order']

    module = models.ForeignKey(
        'Module',
        related_name='contents',
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=
        {
            'model__in': 
            (
                'text',
                'video',
                'image',
                'file',
                'question',
                'blockly',
                'c_plus_plus',
            )
        }
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])


class ItemBase(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE,
        )
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def render(self):
        return render_to_string('courses/content/{}.html'.format(
            self._meta.model_name), {'item': self})

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class Drag_and_drop(ItemBase):
    question = models.TextField()
    answer_1 = models.CharField(max_length=300, default='')
    answer_2 = models.CharField(max_length=300, default='')
    answer_correct = models.CharField(max_length=300, default='')


class Blockly(ItemBase):
    content = models.TextField()
    answer = models.CharField(max_length=300, default='')


class C_plus_plus(ItemBase):
    content = models.TextField()
    answer = models.CharField(max_length=300, default='')


class Question(ItemBase):
    content = models.TextField()
    answer = models.CharField(max_length=300, default='')


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()


opentok = OpenTok("46769324", "0a5d254d5d11b7e1ef22004df51b6e28f9279823")
session = opentok.create_session()

session_id = session.session_id
token = opentok.generate_token(session_id)


class LessonRoom(models.Model):
    """Describe courses_lessonroom table in database.

    ForeignKey because one teacher for many module rooms.
    ManyToMany because many students for many module rooms.

    students: students what are invited to lesson

    duration: how much time goes lesson

    Note: when lesson just goes and teacher.amount += teacher (check for time)

    """

    lesson_name = models.CharField(max_length=200)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)
    session_id = models.CharField(max_length=100, default=session_id)
    token = models.CharField(max_length=400, default=token)
    schedule = models.OneToOneField(
        Schedule,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    homework = models.TextField(blank=True, default='')
    completed = models.BooleanField(default=False)
    duration = models.DurationField(
        blank=True, default=timedelta(minutes=60),
    )

    def __str__(self):
        """Override the str() behavior, for instance of class.

        Returns:
            self.id : Instance id
        """
        return '{0}'.format(self.id)


class Subscription(models.Model):
    """
    student: which student has bought amount of lessons
    lessons_amount: how much lessons in Subscription what student bought
    cost: cost of Subscription

    """

    class TeacherCurrency(models.TextChoices):
        RUBLE = 'RUB', _('Ruble')
        DOLLAR = 'USD', _('Dollar')
        EURO = 'EUR', _('Euro')

    student = models.ForeignKey(
        Student,
        related_name='subscriptions',
        on_delete=models.CASCADE,
    )
    lessons_amount = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=TeacherCurrency.choices,
        default=TeacherCurrency.RUBLE,
    )
    completed = models.BooleanField(default=False)
