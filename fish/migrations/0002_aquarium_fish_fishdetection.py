# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-12 11:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fish', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aquarium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('tank_nbr', models.IntegerField()),
                ('usbs', models.TextField()),
                ('temperatures', models.TextField()),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Fish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfid', models.CharField(max_length=30)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('aquarium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fishes', to='fish.Aquarium')),
            ],
        ),
        migrations.CreateModel(
            name='FishDetection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antenna_number', models.IntegerField()),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('fish_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detections', to='fish.Fish')),
            ],
        ),
    ]