# Generated by Django 5.1.4 on 2025-01-20 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers_app', '0010_delete_singleoffer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerdetail',
            name='title',
            field=models.CharField(default='Basic Design', max_length=255),
        ),
    ]
