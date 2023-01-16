from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import ListCharField

# Create your models here.
class Track(models.Model):
    image = models.FileField(default=None,upload_to='static/images',)
    file = models.FileField(default=None,upload_to='media',)
    title = models.CharField(default='',max_length=200)
    author = models.CharField(default='',max_length=200)
    genres = models.CharField(default='',max_length=200)
    tags = models.CharField(default='',max_length=200)
    price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
    def __unicode__(self):
        return self.title
    
    
class Person(User):
    pass
    buyed = ListCharField(
        default="",
        base_field=models.CharField(default="",max_length=50),
        size=10,
        max_length=(100 * 10),  # 6 * 10 char)
    )
    def __unicode__(self):
        return self.buyed
    
