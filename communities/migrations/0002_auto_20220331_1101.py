# Generated by Django 3.2 on 2022-03-31 11:01

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='bg_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='community_bg_image'),
        ),
        migrations.AddField(
            model_name='community',
            name='logo',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='community_logo'),
        ),
    ]
