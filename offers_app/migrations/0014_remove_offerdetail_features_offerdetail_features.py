# Generated by Django 5.1.4 on 2025-01-21 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers_app', '0013_remove_offerdetail_features_offerdetail_features'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offerdetail',
            name='features',
        ),
        migrations.AddField(
            model_name='offerdetail',
            name='features',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
