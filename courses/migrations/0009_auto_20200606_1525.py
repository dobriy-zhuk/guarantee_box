# Generated by Django 3.0.1 on 2020-06-06 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_auto_20200606_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonroom',
            name='session_id',
            field=models.CharField(default='1_MX40Njc2OTMyNH5-MTU5MTQ1NzEzODcyN35XdUZQSDhJbFRJTW43a2p0TWszN2dQaWx-UH4', max_length=100),
        ),
        migrations.AlterField(
            model_name='lessonroom',
            name='token',
            field=models.CharField(default='T1==cGFydG5lcl9pZD00Njc2OTMyNCZzaWc9ODA4NTU1NWU2OTEyYjM4MDEyZmJhOGY4MTI5MTlkNmUwMGYzZjM1YjpzZXNzaW9uX2lkPTFfTVg0ME5qYzJPVE15Tkg1LU1UVTVNVFExTnpFek9EY3lOMzVYZFVaUVNEaEpiRlJKVFc0M2EycDBUV3N6TjJkUWFXeC1VSDQmY3JlYXRlX3RpbWU9MTU5MTQ1NzEzOCZleHBpcmVfdGltZT0xNTkxNTQzNTM4JnJvbGU9cHVibGlzaGVyJm5vbmNlPTQzNjA4MyZpbml0aWFsX2xheW91dF9jbGFzc19saXN0PQ==', max_length=400),
        ),
    ]
