# Generated by Django 4.1.5 on 2023-01-07 11:34

import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_track_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='author',
            field=django.contrib.postgres.fields.citext.CICharField(default='', max_length=200),
        ),
    ]
