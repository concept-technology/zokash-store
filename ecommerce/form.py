from django import forms
from django_countries.fields import CountryField


class CheckoutForm(forms.Form):
    street_address = forms.CharField(max_length=300)
    house_number = forms.CharField(max_length=255)
    city_or_town = forms.CharField(max_length=255)
    state = forms.CharField(max_length=255)
    zip_code = forms.CharField(max_length=20)
    country = CountryField(blank_label="(select country)")
    deliver_to_different_address = forms.BooleanField(widget=forms.CheckboxInput())
    save_info = forms.BooleanField(widget=forms.CheckboxInput())
    payment_option = forms.BooleanField(widget=forms.RadioSelect())
    def __unicode__(self):
        return self.country
    
# class PaymentOPtion(forms.forms):