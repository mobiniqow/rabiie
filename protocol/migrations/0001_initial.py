# Generated by Django 4.2 on 2024-01-13 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_device', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EVENT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('message', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=25)),
                ('input_output', models.BooleanField()),
                ('ack', models.BooleanField(default=False)),
                ('user_device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_device.userdevice')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]