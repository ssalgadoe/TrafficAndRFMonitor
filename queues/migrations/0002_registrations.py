# Generated by Django 2.0.2 on 2018-02-23 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cust_name', models.CharField(blank=True, max_length=100, null=True)),
                ('ip', models.CharField(blank=True, max_length=45, null=True)),
                ('mac', models.CharField(blank=True, max_length=45, null=True)),
                ('rssi', models.CharField(blank=True, max_length=10, null=True)),
                ('snr', models.CharField(blank=True, max_length=10, null=True)),
                ('ccq_tx', models.CharField(blank=True, max_length=10, null=True)),
                ('ccq_rx', models.CharField(blank=True, max_length=10, null=True)),
                ('uptime', models.CharField(blank=True, max_length=45, null=True)),
                ('time_stamp', models.CharField(blank=True, max_length=45, null=True)),
                ('extra', models.CharField(blank=True, max_length=50, null=True)),
                ('comment', models.CharField(blank=True, max_length=45, null=True)),
            ],
        ),
    ]
