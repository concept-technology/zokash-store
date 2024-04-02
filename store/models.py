from django.db import models
from django.conf import settings


# Create your models here.
from django.urls import reverse
category_choices = (
        ('new', 'new'),
        ('featured', 'featured'),
        ('promo', 'promo'),
        ('ankara', 'ankara'),
        ('shoes', 'shoes'),
        
    )
label_choices = (
    ('new', 'label-new'),
    ('out', 'label-out'),
    ('top', 'label-top'),
)

class Category(models.Model):
    title = models.CharField(max_length=255, choices=category_choices)
    slug = models.SlugField()
    def __str__(self) -> str:
        return f'{self.title}'
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    description= models.TextField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    discount_price = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True, default='')
    main_img  = models.ImageField(upload_to='static/media/img', default='img')
    sub_img1  = models.ImageField(upload_to='static/media/img', default='img')
    sub_img2  = models.ImageField(upload_to='static/media/img', default='img')
    sub_img3  = models.ImageField(upload_to='static/media/img', default='img')
    label = models.CharField(choices=label_choices, max_length=255, default='', blank=True)
    category = models.ForeignKey(Category, default='', on_delete=models.CASCADE)
    slug = models.SlugField( default='')
    
    def get_absolute_url(self):
        return reverse("store:store_item", kwargs={"slug": self.slug})
    
    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart", kwargs={"slug": self.slug})
    
    def delete_cart(self):
        return reverse("store:delete_cart", kwargs={"slug": self.slug})
    
    def __str__(self):
        return f"{self.title} : {self.price}"
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=Product)
    quantity = models.IntegerField(default =1) 
    is_ordered = models.BooleanField(default=False)
    
    
    def __str__(self):
        price = int(self.product.price)
        dis_count_price = int(self.product.discount_price)
        if not dis_count_price:
            return f"product: {self.product.title} price: {price}  quantity: {self.quantity}"
        else:
            return f" product:  {self.product.title}: price: {dis_count_price} quantity: {self.quantity}"
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='' )
    is_ordered = models.BooleanField(default=False)
    product = models.ManyToManyField(Cart)
    ordered_date = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.user.username}"













