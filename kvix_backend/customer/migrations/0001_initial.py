# Generated by Django 3.2.13 on 2022-05-16 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('platform_central', '0001_initial'),
        ('distributor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerGlobal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=255, null=True)),
                ('address_line_1', models.TextField(blank=True, max_length=10000, null=True)),
                ('address_line_2', models.TextField(blank=True, max_length=10000, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('pincode', models.CharField(blank=True, max_length=6, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=10, null=True)),
                ('alternate_mobile_number', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Customer Global',
            },
        ),
        migrations.CreateModel(
            name='CustomerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=255, null=True)),
                ('address_line_1', models.TextField(blank=True, max_length=10000, null=True)),
                ('address_line_2', models.TextField(blank=True, max_length=10000, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('pincode', models.CharField(blank=True, max_length=6, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=10, null=True)),
                ('alternate_mobile_number', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer_global', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customerglobal')),
            ],
            options={
                'verbose_name_plural': 'Customer User',
            },
        ),
        migrations.CreateModel(
            name='CustomerProfilePicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, help_text='profile image', null=True, upload_to='customer_images/%Y/%m/%d')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customeruser')),
            ],
            options={
                'verbose_name_plural': 'Customer Profile Picture',
            },
        ),
        migrations.CreateModel(
            name='CustomerKYCDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], max_length=255, null=True)),
                ('document_file', models.FileField(blank=True, help_text='kyc doc', null=True, upload_to='customer_verification_documents/%Y/%m/%d/')),
                ('document_file_front', models.FileField(blank=True, help_text='kyc doc - front side', null=True, upload_to='customer_verification_front_documents/%Y/%m/%d/')),
                ('document_file_back', models.FileField(blank=True, help_text='kyc doc - back side', null=True, upload_to='customer_verification_back_documents/%Y/%m/%d/')),
                ('is_verified', models.BooleanField(blank=True, default=False, null=True)),
                ('api_response', models.TextField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customeruser')),
                ('document_master', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='platform_central.documentmaster')),
            ],
            options={
                'verbose_name_plural': 'Customer Bank Detail',
            },
        ),
        migrations.CreateModel(
            name='CustomerDistributorMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customeruser')),
                ('distributor_firm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='distributor.distributorfirm')),
            ],
            options={
                'verbose_name_plural': 'Customer Distributor Mapping',
            },
        ),
        migrations.CreateModel(
            name='CustomerBankDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('account_number', models.CharField(blank=True, max_length=255, null=True)),
                ('re_enter_account_number', models.CharField(blank=True, max_length=255, null=True)),
                ('payment_mode', models.CharField(blank=True, choices=[('BANK', 'BANK'), ('UPI', 'UPI')], max_length=255, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=255, null=True)),
                ('branch', models.CharField(blank=True, max_length=255, null=True)),
                ('account_holder_name', models.CharField(blank=True, max_length=255, null=True)),
                ('primary_upi', models.CharField(blank=True, max_length=255, null=True)),
                ('umrn_number', models.CharField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customeruser')),
            ],
            options={
                'verbose_name_plural': 'Customer Bank Detail',
            },
        ),
        migrations.CreateModel(
            name='CustomerApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], max_length=255, null=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customeruser')),
            ],
            options={
                'verbose_name_plural': 'Customer Approval',
            },
        ),
    ]