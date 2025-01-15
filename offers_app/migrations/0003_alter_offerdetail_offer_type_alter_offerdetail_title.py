# Generated by Django 5.1.4 on 2025-01-15 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers_app', '0002_feature_remove_offerdetail_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerdetail',
            name='offer_type',
            field=models.CharField(choices=[('Basic', 'Basic'), ('Standard', 'Standard'), ('Premium', 'Premium')], default='Basic Design', max_length=255),
        ),
        migrations.AlterField(
            model_name='offerdetail',
            name='title',
            field=models.CharField(choices=[('Basic Design', 'Basic Design'), ('Standard Design', 'Standard Design'), ('Premium Design', 'Premium Design')], default='Basic', max_length=255),
        ),
    ]
