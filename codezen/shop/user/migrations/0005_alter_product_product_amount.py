# Generated by Django 4.0.1 on 2022-01-20 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_product_product_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_amount',
            field=models.CharField(max_length=100),
        ),
    ]