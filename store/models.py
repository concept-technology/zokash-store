from django.db import models
from django.conf import settings



label_choices= (
    ('top', 'top'),
    ('new', 'new'),
    ('featured', 'featured'),
    ('out', 'out'),
)

class Category(models.Model):
    title = models.CharField(max_length=255)

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=0, max_digits=9)
    discount_price = models.DecimalField(decimal_places=0, max_digits=9)
    description = models.TextField(max_length=1000)
    label = models.CharField(max_length=255, choices=label_choices)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    display_on_home_page = models.BooleanField(default=False)
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ManyToManyField(Cart)
    date = models.DateField( auto_now=False, auto_now_add=False)
    is_ordered = models.BooleanField(default=False)