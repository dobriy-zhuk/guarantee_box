# Generated by Django 3.0.1 on 2020-04-19 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_auto_20200419_2113'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StudentStatus',
        ),
        migrations.AddField(
            model_name='student',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
