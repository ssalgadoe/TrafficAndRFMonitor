# Generated by Django 2.0.2 on 2018-03-16 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0015_auto_20180313_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue_data',
            name='time_delta',
            field=models.CharField(blank=True, default='1', max_length=15, null=True),
        ),
    ]
