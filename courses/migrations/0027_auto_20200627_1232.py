# Generated by Django 3.0.1 on 2020-06-27 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0026_auto_20200627_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonroom',
            name='session_id',
            field=models.CharField(default='1_MX40Njc2OTMyNH5-MTU5MzI1MDM0MTY0NX45THAzd1NGVXZEaThqcmdHdkFndDBualR-UH4', max_length=100),
        ),
        migrations.AlterField(
            model_name='lessonroom',
            name='token',
            field=models.CharField(default='T1==cGFydG5lcl9pZD00Njc2OTMyNCZzaWc9YzMwYzI3NmExOGU5NGFiMmMwNTAyNDZmMTdhYWI5ODAzNTU3NmQyMDpzZXNzaW9uX2lkPTFfTVg0ME5qYzJPVE15Tkg1LU1UVTVNekkxTURNME1UWTBOWDQ1VEhBemQxTkdWWFpFYVRocWNtZEhka0ZuZERCdWFsUi1VSDQmY3JlYXRlX3RpbWU9MTU5MzI1MDM0MSZleHBpcmVfdGltZT0xNTkzMzM2NzQxJnJvbGU9cHVibGlzaGVyJm5vbmNlPTUyMzM3MSZpbml0aWFsX2xheW91dF9jbGFzc19saXN0PQ==', max_length=400),
        ),
    ]
