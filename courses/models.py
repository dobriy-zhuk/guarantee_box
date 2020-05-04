"""File with classes which describe tables in database."""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    # TODO: атрибус пройден/непройден
    # TODO: Отправка информации о прохождении курсов, выполнении дз и полной статистики на емайл
    owner = models.ForeignKey(
        User,
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
        User,
        related_name='courses_joined',
        blank=True,
        )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    class Meta:
        ordering = ['order']
        permissions = (
                ('view_current_module', 'Can view current module'),
            )

    course = models.ForeignKey(
        Course,
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
        Module,
        related_name='contents',
        on_delete=models.CASCADE,
        )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': (
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

