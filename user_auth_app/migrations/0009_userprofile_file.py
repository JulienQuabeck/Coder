# Generated by Django 5.1.4 on 2025-01-08 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth_app', '0008_fileupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
