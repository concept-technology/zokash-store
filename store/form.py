from django import forms
from django_countries.fields import CountryField
from  django_countries.widgets import CountrySelectWidget
payment_choices= (
    ('paypal', 'paypal'),
    ('paystack', 'paystack'),
    ('ussd transfer', 'ussd transfer'),
    ('mobile transfer', 'mobile transfer')
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
    