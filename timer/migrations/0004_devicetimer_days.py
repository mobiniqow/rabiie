# Generated by Django 4.1.1 on 2024-11-26 14:13

from django.db import migrations, models
import timer.models


class Migration(migrations.Migration):

    dependencies = [
        ("timer", "0003_alter_devicetimer_unique_together_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="devicetimer",
            name="days",
            field=models.CharField(
                default=1, max_length=7, validators=[timer.models.day_validator]
            ),
            preserve_default=False,
        ),
    ]