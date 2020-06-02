# Generated by Django 3.0.1 on 2020-06-02 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_studentrewardcard_teacher'),
        ('courses', '0003_course_course_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_name', models.CharField(max_length=200)),
                ('session_id', models.CharField(default='', max_length=100)),
                ('token', models.CharField(default='', max_length=400)),
                ('students', models.ManyToManyField(blank=True, to='students.Student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Teacher')),
            ],
        ),
        migrations.DeleteModel(
            name='ZoomModuleRoom',
        ),
    ]
