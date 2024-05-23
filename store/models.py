import secrets
from django.db import models
from django.conf import settings
from django.shortcuts import redirect
from django_countries.fields import CountryField
from django_countries import countries
from .paystack import Paystack

# from django.utils import timezone

from django.urls import reverse
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
    ('ussd transfer', 'ussd transfer'),
    ('mobile transfer', 'mobile transfer')
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
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
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
            



class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='' )
    street_address = models.CharField(max_length=300)
    apartment = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    # telephone= models.IntegerField(default=0)
    zip_code = models.CharField(max_length=20)
    country = CountryField(multiple=False)
    payment_option = models.CharField(max_length=255, choices=payment_choices)
   
    def __str__(self):
       return self.user.username
   

    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='' )
    is_ordered = models.BooleanField(default=False)
    product = models.ManyToManyField(Cart,)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f" {self.user.username}, address:  {self.billing_address}"
    


    # display the quantity in table
    def quantity(self):
        for items in self.product.all():
            return items.quantity
        return None
    
    def get_total(self):
        total = 0
        for items in self.product.all():
            total += items.get_total_price()
        return total
    
        # display the product title in datable
    def number_of_items(request):
        queryset = Cart.objects.filter(user=request.user, is_ordered=False).count()
        if queryset == 0:
            return '-'
        return queryset
    
        # get the price in the order
    def total_price(self):
        return self.get_total()
    
    
    
    
    
    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, default='', null=True, blank=True)
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
        amount = int(self.amount * 100)
        return amount

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, int(self.amount))
        if status:
            if int(result['amount']) / 100 == int(self.amount):
                self.verified = True
                self.save()
            self.verified = False
        return status
        
    
    
    

    

         

