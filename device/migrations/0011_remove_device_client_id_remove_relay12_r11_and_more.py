# Generated by Django 4.2.3 on 2024-01-29 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0010_alter_device_client_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='client_id',
        ),
        migrations.RemoveField(
            model_name='relay12',
            name='r11',
        ),
        migrations.RemoveField(
            model_name='relay12',
            name='r12',
        ),
        migrations.AddField(
            model_name='relay12',
            name='client_id',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AddField(
            model_name='relay6',
            name='client_id',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]