# Generated by Django 2.0.2 on 2018-02-27 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0008_queue_data_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue_data',
            name='usage',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]
