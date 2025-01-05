# Generated by Django 5.1.2 on 2025-01-04 22:13

import account.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_account_type_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to=account.models.user_directory_path)),
                ('image_order', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_images', to='account.profile')),
            ],
        ),
    ]