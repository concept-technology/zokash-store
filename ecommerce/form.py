from django import forms
from .models import Address

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
