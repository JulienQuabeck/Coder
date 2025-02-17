# Generated by Django 5.1.4 on 2025-01-24 16:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0004_alter_orders_offer_detail_id_alter_orders_status'),
        ('user_auth_app', '0019_alter_fileupload_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_user', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('revisions', models.IntegerField()),
                ('delivery_time_in_days', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=4, max_digits=5)),
                ('features', models.JSONField()),
                ('offer_type', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('in_progress', 'in_progress'), ('completed', 'completed'), ('cancelled', 'cancelled')], default='in_progress', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_auth_app.userprofile')),
            ],
        ),
    ]
