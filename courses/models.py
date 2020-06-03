"""File with classes which describe tables in database."""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from courses.fields import OrderField
from django.template.loader import render_to_string
from students.models import Student, Teacher, Schedule


class Subject(models.Model):
    """Describe the courses_subject table in database.

    Subject is the theme of lesson.

    Arguments:
        models.Model: superclass where describe the fields
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

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


    Arguments:
        models.Model: superclass where describe the fields
    """

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
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(
        Student,
        related_name='courses_joined',
        blank=True,
    )
    course_image = models.ImageField(blank=True, default='')


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
        
        You need to specifi the instanse for permission
        student.user.has_perm('module_done', module)
        True

        get_objects_for_user(student.user, 'courses.module_done')
                                              ^
                                    name of app required
        <QuerySet [<Module: 0. Переменные>]>

    Arguments:
        models {[type]} -- [description]

    Returns:
        [type] -- [description]
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
    title = models.CharField(max_length=250)
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


class LessonRoom(models.Model):
    """Describe courses_lessonroom table in database.

    ForeignKey because one teacher for many module rooms.
    ManyToMany because many students for many module rooms.
    TODO: TextField homework 

    Arguments:
        models.Model: superclass which describes fields for database
    """

    lesson_name = models.CharField(max_length=200)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)
    session_id = models.CharField(max_length=100, default='')
    token = models.CharField(max_length=400, default='')
    schedule = models.OneToOneField(
        Schedule,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        """Override the str() behavior, for instance of class.

        Returns:
            self.module_name: Instance module_name
        """
        return self.lesson_name
