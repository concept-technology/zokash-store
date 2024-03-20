from django.db import models
from django.conf import settings
# Create your models here.


class Item(models.Model):
    title = models.CharField(max_length=255)
    description= models.TextField(max_length=1000)
    color =models.CharField(max_length=255)
    price = models.FloatField()
    
class Cart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    item = models.ManyToManyField(Cart)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()