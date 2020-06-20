# Generated by Django 3.0.1 on 2020-06-20 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20200620_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonroom',
            name='session_id',
            field=models.CharField(default='1_MX40Njc2OTMyNH5-MTU5MjY4NTUzMDg1M35GbW5nV3R6VFhnRXBhWE9FY0tySEpSaEx-UH4', max_length=100),
        ),
        migrations.AlterField(
            model_name='lessonroom',
            name='token',
            field=models.CharField(default='T1==cGFydG5lcl9pZD00Njc2OTMyNCZzaWc9NThlYTllMWJmMzUzMDMyNjA3OTkxMTVmZmQ2YjkxYmI1NWUyNzc5ZTpzZXNzaW9uX2lkPTFfTVg0ME5qYzJPVE15Tkg1LU1UVTVNalk0TlRVek1EZzFNMzVHYlc1blYzUjZWRmhuUlhCaFdFOUZZMHR5U0VwU2FFeC1VSDQmY3JlYXRlX3RpbWU9MTU5MjY4NTUzMCZleHBpcmVfdGltZT0xNTkyNzcxOTMwJnJvbGU9cHVibGlzaGVyJm5vbmNlPTQ3NjU2MyZpbml0aWFsX2xheW91dF9jbGFzc19saXN0PQ==', max_length=400),
        ),
        migrations.DeleteModel(
            name='Testimonials',
        ),
    ]
