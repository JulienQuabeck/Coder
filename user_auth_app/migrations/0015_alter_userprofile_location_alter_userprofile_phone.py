# Generated by Django 5.1.4 on 2025-01-09 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth_app', '0014_alter_userprofile_description_alter_userprofile_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=13, null=True),
        ),
    ]