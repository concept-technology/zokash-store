from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    img = models.ImageField(upload_to='blog/img', default='')
    