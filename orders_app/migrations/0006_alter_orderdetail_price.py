# Generated by Django 5.1.4 on 2025-02-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0005_orderdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
