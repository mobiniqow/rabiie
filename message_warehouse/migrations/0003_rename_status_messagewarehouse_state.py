# Generated by Django 4.2.3 on 2024-02-01 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message_warehouse', '0002_remove_messagewarehouse_client'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messagewarehouse',
            old_name='status',
            new_name='state',
        ),
    ]