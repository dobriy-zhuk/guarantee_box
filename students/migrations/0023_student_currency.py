# Generated by Django 3.0.1 on 2020-04-19 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0022_student_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='currency',
            field=models.CharField(default='RUB', max_length=3),
        ),
    ]
