# Generated by Django 4.0.4 on 2022-05-24 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('platform_central', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.SlugField(max_length=255, unique=True)),
                ('role_status', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'System Roles',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('key', models.CharField(blank=True, db_index=True, max_length=40, unique=True, verbose_name='Key')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_tokens', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Tokens',
                'db_table': 'rest_framework_authtoken_model_token',
            },
        ),
        migrations.CreateModel(
            name='AttemptsChecker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempts_left', models.CharField(blank=True, default=3, max_length=4, null=True)),
                ('retry_after_timestamp', models.DateTimeField(blank=True, null=True)),
                ('is_success', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('otp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='platform_central.otp')),
            ],
        ),
    ]