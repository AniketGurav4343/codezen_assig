# Generated by Django 4.0.1 on 2022-01-20 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_platformapicall_requested_data_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='amount',
            new_name='product_amount',
        ),
    ]