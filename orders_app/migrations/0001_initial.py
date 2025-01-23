# Generated by Django 5.1.4 on 2025-01-23 05:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_auth_app', '0019_alter_fileupload_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_user', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=255)),
                ('revisions', models.IntegerField(default=0)),
                ('delivery_time_in_days', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('features', models.JSONField(blank=True, default=dict)),
                ('offer_type', models.CharField(choices=[('basic', 'basic'), ('standard', 'standard'), ('premium', 'premium')], default='basic', max_length=255)),
                ('status', models.CharField(choices=[('in_progres', 'in_progress'), ('completed', 'completed')], default='in_progress', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_auth_app.userprofile')),
            ],
        ),
    ]
