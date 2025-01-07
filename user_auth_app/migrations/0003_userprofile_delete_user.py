# Generated by Django 5.1.4 on 2025-01-07 21:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth_app', '0002_user_delete_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
                ('repeated_password', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('business', 'Business'), ('customer', 'Customer')], default='customer', max_length=8)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
