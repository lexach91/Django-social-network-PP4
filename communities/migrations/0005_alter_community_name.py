# Generated by Django 3.2 on 2022-05-18 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0004_auto_20220514_0356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
