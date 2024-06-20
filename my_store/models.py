import secrets
from django.db import models
from django.conf import settings
from django.utils import dates
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from django.utils import timezone
from django.core.validators import RegexValidator

# from django.utils import timezone

from django.urls import reverse

import humanize
category_choices = (
        ('new', 'new'),
        ('featured', 'featured'),
        ('promo', 'promo'),
        ('ankara', 'ankara'),
        ('shoes', 'shoes'),
        
    )

payment_choices= (
    ('paypal', 'paypal'),
    ('paystack', 'paystack'),
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
    title = models.CharField(max_length=255,)
    slug =models.SlugField(default='')
    
    def save(self, *args, **kwargs):
        self.slug = self.slug 
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.title}'
    
    def get_absolute_url(self):
        return reverse("store:categories-filter", kwargs={"slug": self.pk})
    
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    description= models.TextField(max_length=1000)
    additional_information= models.TextField(max_length=1000, default='')
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    img_1  = models.ImageField(upload_to='static/media/img', default='img')
    img_2  = models.ImageField(upload_to='static/media/img', default='img', blank=True, null=True)
    img_3  = models.ImageField(upload_to='static/media/img', default='img',blank=True, null=True)
    img_4  = models.ImageField(upload_to='static/media/img', default='img',blank=True, null=True)
    label = models.CharField(choices=label_choices, max_length=255, default='', blank=True)
    category = models.ForeignKey(Category, default='', on_delete=models.CASCADE)
    slug = models.SlugField( default=title)
    gender= models.CharField(max_length=10, choices=gender_choices, default='female', blank=True, null=True)
    display_on_home_page =models.BooleanField(default=False)
    is_banner =models.BooleanField(default=False)
    is_best_selling = models.BooleanField(default=False)
   
    def get_absolute_url(self):
        return reverse("store:store_item", kwargs={"slug": self.slug})
    
    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart", kwargs={"slug": self.slug})
    
    def delete_cart(self):
        return reverse("store:delete_cart", kwargs={"slug": self.slug,})
    
    def get_cart_increment(self):
        return reverse("store:reduce_cart", kwargs={"slug": self.slug,})
    
    def get_cart_increment(self):
        return reverse("store:increase_cart", kwargs={"slug": self.slug,})

    def __str__(self):
        return f"{self.title}"
    
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
        
    def add_quantity(self):
        qty = self.quantity
        qty +=1
        return qty
    
    def __str__(self):
        price = self.product.price
        dis_count_price = self.product.discount_price
        title = self.product.title
        if not dis_count_price:
            return f"item: {title}, price: {price}, quantity: {self.quantity}"        
        return f"item:{title} price: {dis_count_price}, quantity: {self.quantity}"
            

    def get_title(self):
        return self.product.title

address_choices =(
    ('shipping', 'shipping Address'),
    ('billing', 'billing Address')
)

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)


class CustomersAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='' )
    street_address = models.CharField(max_length=300)
    apartment = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    telephone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    zip_code = models.CharField(max_length=20)
    country = CountryField(multiple=False)
    payment_option = models.CharField(max_length=255, choices=payment_choices, blank=True,null=True)
   
    def __str__(self):
       return f"{self.user.username}:   address is {self.street_address}" 
   
    def get_absolute_url(self):
        return reverse("store:update-address", kwargs={"pk": self.pk})
    
    
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='' )
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Payment: {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(10)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref

        super().save(*args, **kwargs)
        
        
    def amount_value(self):
        return int(self.amount) * 100

class ShippingMethod(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - N{self.cost} (Delivery in {self.delivery_time})"

    
   
    

class Coupon(models.Model):
    code = models.CharField(max_length=50)
    amount = models.IntegerField(default=0,)
    valid_from = models.DateTimeField(default=timezone.now())
    valid_to = models.DateTimeField(default=timezone.now(), blank=True, null=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='' ,blank=True,null=True)
    is_used = models.BooleanField(default=False)
    used_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='used_coupons', blank=True)
 
    def __str__(self) -> str:
        return f"{self.code}   {self.amount}"
del_status = (
    ('processing', 'processing'),
    ('in_progress', 'in_progress'),
    ('delivered', 'delivered'),
)      
     
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='' )
    is_ordered = models.BooleanField(default=False)
    product = models.ManyToManyField(Cart,)
    reference = models.CharField(max_length=50, default='')
    shipping_address = models.ForeignKey(CustomersAddress, on_delete=models.SET_NULL, blank=True, null=True)
    Payment = models.ForeignKey(Payment, on_delete=models.PROTECT, blank=True, null=True)
    coupon = models.ForeignKey(Coupon,  on_delete=models.SET_NULL, blank=True, null=True)
    is_delivered = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
    is_refund_request = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.datetime.now())
    delivery_status = models.CharField(max_length=255, default='Processing',choices=del_status)
    
    def __str__(self):
        return f" {self.user.username}, address:  {self.Payment}"
    

    # display the quantity in table
    def quantity(self):
        for items in self.product.all():
            return items.quantity
        return None
    
    def get_total(self):
        total = 0
        for item in self.product.all():
            total += item.get_total_price()
        if self.coupon:
            total -= self.coupon.amount
        return total 
    
    def get_coupon(self):
 
        return self.get_total() - self.coupon.amount
  
        # display the product title in datable
    def number_of_items(self):
        queryset = Cart.objects.filter(user=self.user, is_ordered=False).count()
        if queryset == 0:
            return '-'
        return queryset
    
    def items(self):
        queryset = self.product.count()
        if queryset == 0:
            return '-'
        return queryset
    
        # get the price in the order
    def total_price(self):
        return self.get_total()


class Refunds(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField(default= '')
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    
    def __str__(self) -> str:
        return f"{self.order} {self.reason}"
    
    
class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return f"{self.product} {self.quantity}"
    