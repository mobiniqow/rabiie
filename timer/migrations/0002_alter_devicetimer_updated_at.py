# Generated by Django 4.1.1 on 2024-11-16 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("timer", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="devicetimer",
            name="updated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]