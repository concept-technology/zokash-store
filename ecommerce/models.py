from django.db import models
from django.conf import settings
# from django.utils import timezone


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
gender_choices =(
    ('Male', 'male'),
    ('Female', 'female'),
)

class Category(models.Model):
    title = models.CharField(max_length=255, choices=category_choices)
    def __str__(self) -> str:
        return f'{self.title}'
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    description= models.TextField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    discount_price = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True, default='')
    img_1  = models.ImageField(upload_to='static/media/img', default='img')
    img_2  = models.ImageField(upload_to='static/media/img', default='img')
    img_3  = models.ImageField(upload_to='static/media/img', default='img')
    img_4  = models.ImageField(upload_to='static/media/img', default='img')
    label = models.CharField(choices=label_choices, max_length=255, default='', blank=True)
    category = models.ForeignKey(Category, default='', on_delete=models.CASCADE)
    slug = models.SlugField( default=title)
    gender= models.CharField(max_length=10, choices=gender_choices, default='female')
    display_on_home_page =models.BooleanField(default=False)
    is_banner =models.BooleanField(default=False)
    is_best_selling = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse("store:store_item", kwargs={"slug": self.slug})
    
    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart", kwargs={"slug": self.slug})
    
    def delete_cart(self):
        return reverse("store:delete_cart", kwargs={"slug": self.slug,})

    
    def __str__(self):
        return f"{self.title} : {self.price}"
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,)
    quantity = models.IntegerField(default =1) 
    is_ordered = models.BooleanField(default=False)
    
    def get_discount_price(self):
        return self.quantity * self.product.discount_price
    
    
    def get_normal_price(self):
        return self.quantity * self.product.price
            
    def get_amount_saved(self):
        return self.get_normal_price() - self.get_discount_price()
    
    def get_price_tag(self):
        discount_price = self.product.discount_price
        normal_price = self.product.price
        if discount_price:
            return discount_price
        return normal_price
        
    
    def get_total_price(self):
        if self.get_discount_price():
            return self.get_discount_price()
        return self.get_normal_price()
        
     
    def __str__(self):
        price = self.product.price
        dis_count_price = self.product.discount_price
        if not dis_count_price:
            return f"product: {self.product.title} price: {price}  quantity: {self.quantity}"
        else:
            return f" product:  {self.product.title}: price: {dis_count_price} quantity: {self.quantity}"
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='' )
    is_ordered = models.BooleanField(default=False)
    product = models.ManyToManyField(Cart)
    def __str__(self) -> str:
        return f"{self.user.username}"
    
    def get_order(self):
        total = 0
        qs = self.product.all()
        return sum(qs.get_total_price(),total)