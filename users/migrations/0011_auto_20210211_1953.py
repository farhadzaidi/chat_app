# Generated by Django 3.1.6 on 2021-02-12 00:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0010_auto_20210211_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendship',
            name='creator',
        ),
        migrations.AddField(
            model_name='friendship',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='friendship',
            name='friend',
        ),
        migrations.AddField(
            model_name='friendship',
            name='friend',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='friend', to=settings.AUTH_USER_MODEL),
        ),
    ]
