# Generated by Django 5.1.2 on 2025-01-06 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profileimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileimages',
            name='description',
            field=models.TextField(null=True),
        ),
    ]