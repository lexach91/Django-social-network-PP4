# Generated by Django 3.2 on 2022-05-14 07:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0004_auto_20220514_0356'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0004_commentevent_likedislikeevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemoveFriendEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiated_remove_friend_events', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targeted_remove_friend_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='FriendRequestEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiated_friend_request_events', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targeted_friend_request_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='FriendEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiated_friend_events', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targeted_friend_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CommunityLeaveEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_leave_events', to='communities.community')),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiated_community_leave_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CommunityJoinEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_join_events', to='communities.community')),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiated_community_join_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CommunityDeleteEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_delete_events', to='communities.community')),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiated_community_delete_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CommunityCreateEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_create_events', to='communities.community')),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiated_community_create_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]