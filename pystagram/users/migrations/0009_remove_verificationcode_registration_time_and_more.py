# Generated by Django 4.2.9 on 2024-01-30 07:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_verificationcode_registration_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verificationcode',
            name='registration_time',
        ),
        migrations.AddField(
            model_name='verificationcode',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]