from django.db import models
from .views import PayStack
import secrets

from django.conf import settings
# Create your models here.

class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.CASCADE, default='')
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    ref =models.CharField(max_length=255)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return f"{self. user} {self.amount}"
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref =Payments.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref =ref
            super().save(*args, **kwargs)
    
    
    def amount_value(self):
        return int(self.amount) * 100
    
    
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:           
            if result['amount'] / 100 == self.amount:
                self.verified ==True
                self.save()
        if self.verified:
            return True
        return  False
    