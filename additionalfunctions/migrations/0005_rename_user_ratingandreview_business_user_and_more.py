# Generated by Django 5.1.4 on 2025-01-28 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('additionalfunctions', '0004_remove_ratingandreview_average_rating_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ratingandreview',
            old_name='user',
            new_name='business_user',
        ),
        migrations.RenameField(
            model_name='ratingandreview',
            old_name='review',
            new_name='description',
        ),
    ]
