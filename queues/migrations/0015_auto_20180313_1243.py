# Generated by Django 2.0.2 on 2018-03-13 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0014_auto_20180313_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue_data',
            name='owner',
            field=models.CharField(blank=True, default='1', max_length=45, null=True),
        ),
    ]
