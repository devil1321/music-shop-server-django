# Generated by Django 4.1.5 on 2023-01-16 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_track_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='stripe_product_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]