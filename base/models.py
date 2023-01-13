from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres import fields
# Create your models here.
class Track(models.Model):
    image = models.FileField(default=None,upload_to='static/images',)
    file = models.FileField(default=None,upload_to='media',)
    title = fields.CICharField(default="",max_length=200,)
    author = fields.CICharField(default="",max_length=200,)
    genres = fields.CICharField(default="",max_length=200,)
    tags = fields.CICharField(default="",max_length=200,)
class Person(User):
    pass
    buyed = fields.ArrayField(base_field=fields.CICharField(max_length=200),blank=True,null=True)