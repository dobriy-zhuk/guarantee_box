# Generated by Django 3.0.1 on 2020-06-27 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0010_student_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='birthday',
            field=models.DateField(null=True),
        ),
    ]
