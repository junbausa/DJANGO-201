# Generated by Django 5.0.1 on 2024-01-22 05:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('followers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Followers',
            new_name='Follower',
        ),
    ]