# Generated by Django 2.0.2 on 2018-02-23 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0003_delete_registrations'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Queues',
        ),
    ]