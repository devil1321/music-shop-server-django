# Generated by Django 4.1.5 on 2023-01-06 20:35

import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_track_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='time',
            field=django.contrib.postgres.fields.citext.CICharField(default='0.00', max_length=4),
        ),
    ]