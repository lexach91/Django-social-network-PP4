# Generated by Django 3.2 on 2022-05-16 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0007_commentevent_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communitydeleteevent',
            name='community',
        ),
    ]
