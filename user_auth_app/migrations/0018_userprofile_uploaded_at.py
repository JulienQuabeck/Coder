# Generated by Django 5.1.4 on 2025-01-10 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth_app', '0017_rename_phone_userprofile_tel'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]