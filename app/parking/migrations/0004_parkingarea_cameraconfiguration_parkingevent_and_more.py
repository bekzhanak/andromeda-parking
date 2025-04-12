# Generated by Django 5.1.7 on 2025-04-12 14:38

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0003_alter_parkingsessionmodel_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CameraConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_name', models.CharField(max_length=255, unique=True)),
                ('direction', models.CharField(choices=[('IN', 'Entering'), ('OUT', 'Exiting')], max_length=3)),
                ('parking_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cameras', to='parking.parkingarea')),
            ],
        ),
        migrations.CreateModel(
            name='ParkingEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('IN', 'Entering'), ('OUT', 'Exiting')], max_length=3)),
                ('event_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('parking_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='parking.parkingsessionmodel')),
            ],
        ),
        migrations.CreateModel(
            name='CarImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate', models.CharField(max_length=20)),
                ('car_image', models.TextField(help_text='Base64 encoded image of the car.')),
                ('captured_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('camera_configuration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='parking.cameraconfiguration')),
                ('parking_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_images', to='parking.parkingevent')),
            ],
        ),
    ]
