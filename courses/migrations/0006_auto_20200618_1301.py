# Generated by Django 3.0.1 on 2020-06-18 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20200617_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonroom',
            name='session_id',
            field=models.CharField(default='1_MX40Njc2OTMyNH5-MTU5MjQ3NDQ3OTEzMX41UHV4QnNhWWcrelFmaHBqYVllR2J4emJ-UH4', max_length=100),
        ),
        migrations.AlterField(
            model_name='lessonroom',
            name='token',
            field=models.CharField(default='T1==cGFydG5lcl9pZD00Njc2OTMyNCZzaWc9NjJkNDRkMjkxMmI1ZmRkYWRlZjVkZDRhNjFkMzAwODg0MDU5YTE4NDpzZXNzaW9uX2lkPTFfTVg0ME5qYzJPVE15Tkg1LU1UVTVNalEzTkRRM09URXpNWDQxVUhWNFFuTmhXV2NyZWxGbWFIQnFZVmxsUjJKNGVtSi1VSDQmY3JlYXRlX3RpbWU9MTU5MjQ3NDQ3OSZleHBpcmVfdGltZT0xNTkyNTYwODc5JnJvbGU9cHVibGlzaGVyJm5vbmNlPTI2MTQ1OSZpbml0aWFsX2xheW91dF9jbGFzc19saXN0PQ==', max_length=400),
        ),
    ]