# Generated by Django 4.0 on 2023-04-29 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='codingtask',
            name='initial_file',
            field=models.FileField(blank=True, null=True, upload_to='initials/'),
        ),
    ]