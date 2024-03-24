from django.db import models
from django.conf import settings
# Create your models here.


class Item(models.Model):
    title = models.CharField(max_length=255)
    description= models.TextField(max_length=1000)
    price = models.FloatField()
    main_img  = models.ImageField(upload_to='static/media/img', default='img')
    sub_img1  = models.ImageField(upload_to='static/media/img', default='img')
    sub_img2  = models.ImageField(upload_to='static/media/img', default='img')
    sub_img3  = models.ImageField(upload_to='static/media/img', default='img')
    
    
    
    def __str__(self) -> str:
        return f"{self.title} : {self.price}"
    
class Cart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        return f"{self.add_to_class}"
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    item = models.ManyToManyField(Cart)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    
    def __str__(self) -> str:
        return f"{self.user} ordered for {self.item}"