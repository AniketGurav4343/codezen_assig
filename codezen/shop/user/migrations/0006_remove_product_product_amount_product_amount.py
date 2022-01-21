# Generated by Django 4.0.1 on 2022-01-20 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_product_product_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_amount',
        ),
        migrations.AddField(
            model_name='product',
            name='amount',
            field=models.FloatField(default=234234),
            preserve_default=False,
        ),
    ]
