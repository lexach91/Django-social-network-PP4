# Generated by Django 3.2 on 2022-05-14 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0003_community_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='description',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='community',
            name='name',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]