from django import forms
from django_countries.fields import CountryField
from  django_countries.widgets import CountrySelectWidget

payment_choices= (
    ('paypal', 'paypal'),
    ('paystack', 'paystack'),

)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs=(
        {
            'placeholder':'street name',
            'class': 'form-control',
            'required': True
        }
    )))
    apartment = forms.CharField(widget=forms.TextInput(attrs=(
        {
            'placeholder':'apartments, suite, unit etc ...',
            'class': 'form-control',
            'required': True
        }
    )))
    town =forms.CharField(widget=forms.TextInput(attrs=(
        {
            'class': 'form-control',
            'required': True
        }
    )))
    state = forms.CharField(widget=forms.TextInput(attrs=(
        {
            'class': 'form-control',
            'required': True
        }
    )))
    # telephone = forms.CharField(widget=forms.TextInput(attrs=(
    #     {
    #         'class': 'form-control',
    #         'required': True
    #     }
    # )))
    country = CountryField(blank_label="select_country").formfield(widget=CountrySelectWidget(attrs=(
        {
            'class': 'from-control'
        }
    )))
       
    zip_code =forms.CharField(widget=forms.TextInput(attrs=(
        {
            'class': 'form-control',
            'required': True
        }
    )),max_length=10)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(),choices=payment_choices)


class CouponForm(forms.Form):
       code =forms.CharField(widget=forms.TextInput(attrs=(
        {
            'class': 'form-control',
            'required': True,
            'placeholder': 'Have a coupon? Click here to enter your code'
        }
    )),max_length=10)


class RefundRequestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs=(
        {
            'class': 'form-control',
            'required': True,
            'placeholder': 'email' 
        }
        )))
    reference_code =forms.CharField(widget=forms.TextInput(attrs=(
        {
            'class': 'form-control',
            'required': True,
            'placeholder': 'order reference'
        }
        )),max_length=15)
    message =forms.CharField(widget=forms.Textarea(attrs=(
        {
            'class': 'form-control',
            'required': True,
            'placeholder': 'reason for refund'
        }
    )),max_length=1000)
    
   
        
    