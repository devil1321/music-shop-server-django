# Generated by Django 4.1.5 on 2023-01-07 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_track_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='image',
            field=models.FileField(default=None, upload_to='static/images'),
        ),
    ]
