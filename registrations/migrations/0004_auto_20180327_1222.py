# Generated by Django 2.0.2 on 2018-03-27 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0003_auto_20180323_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
                ('address', models.CharField(blank=True, max_length=60, null=True)),
                ('lon_id', models.CharField(blank=True, max_length=20, null=True)),
                ('lat_id', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='aps',
            name='lat_id',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='aps',
            name='lon_id',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]
