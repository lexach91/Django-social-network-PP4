# Generated by Django 3.2 on 2022-04-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='has_media',
            field=models.BooleanField(default=False),
        ),
    ]
