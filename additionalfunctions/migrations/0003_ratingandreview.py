# Generated by Django 5.1.4 on 2025-01-28 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('additionalfunctions', '0002_ordercount_order_count'),
        ('user_auth_app', '0019_alter_fileupload_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingAndReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_count', models.IntegerField()),
                ('average_rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_auth_app.userprofile')),
            ],
        ),
    ]
