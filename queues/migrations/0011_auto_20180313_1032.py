# Generated by Django 2.0.2 on 2018-03-13 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0010_auto_20180227_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue_data',
            name='dummy',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='registrations',
            name='dummy',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
