# Generated by Django 2.0.2 on 2018-03-21 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrations',
            old_name='ap_id',
            new_name='ap',
        ),
    ]
