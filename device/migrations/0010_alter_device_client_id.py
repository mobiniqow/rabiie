# Generated by Django 4.2.3 on 2024-01-28 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0009_device_client_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='client_id',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]