# Generated by Django 4.2.9 on 2024-02-02 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=200, verbose_name='내용'),
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(max_length=300, verbose_name='내용'),
        ),
    ]
