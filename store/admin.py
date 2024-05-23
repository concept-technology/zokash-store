from django.contrib import admin
from .models import Product,Cart,Order, Category, BillingAddress
from django.utils.html import format_html

from .models  import  Payment

class  PaymentAdmin(admin.ModelAdmin):
    list_display  = ['order', "ref", 'amount', "verified", "date_created"]

admin.site.register(Payment, PaymentAdmin)


class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:50px; max-height:100px"/>'.format(obj.img_1.url))
    list_display = ['title', 'image_tag', 'price', 'discount_price']
    image_tag.short_description = 'Image'
    

class CartAdmin(admin.ModelAdmin):    
    list_display = ['product', 'user', 'get_price_tag'] 
    class Meta:
        Model= Cart
                    



class OrderAdmin(admin.ModelAdmin):
    list_display= [ 'user','number_of_items','total_price','is_ordered',]
    readonly_fields = ('user',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


class AddressAdmin(admin.ModelAdmin):
    list_display = '__all__'





admin.site.register(Product, ProductAdmin) 
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.register(BillingAddress)
