# Generated by Django 3.2 on 2022-05-10 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20220404_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pending_friends_in',
            field=models.ManyToManyField(blank=True, related_name='_profiles_profile_pending_friends_in_+', to='profiles.Profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='pending_friends_out',
            field=models.ManyToManyField(blank=True, related_name='_profiles_profile_pending_friends_out_+', to='profiles.Profile'),
        ),
    ]
