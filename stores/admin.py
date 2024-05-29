from django.contrib import admin
from .models import Product,Cart,Order, Category,CustomersAddress, Coupon, Refunds
from django.utils.html import format_html

from .models  import  Payment

class  PaymentAdmin(admin.ModelAdmin):
    list_display  = ["user","ref",'amount', "verified", "date_created"]

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
                    

class make_accept_refund(admin.ModelAdmin, ):
    autocomplete_fields = ['is_refund_request', 'refund_granted']


make_accept_refund.short_description = 'update refund granted'
    

class OrderAdmin(admin.ModelAdmin):
    list_display= [ 'user','items','total_price','reference','is_ordered','is_delivered', 'is_received', 'is_refund_request', 'refund_granted']
    readonly_fields = ('user',)
    list_filter =  [ 'is_ordered','is_delivered', 'is_received', 'is_refund_request', ]
    
    list_display_links = ['user','items',]
    search_fields = ['user__username', 'reference']
    
    
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


class AddressAdmin(admin.ModelAdmin):
    list_display = '__all__'


class CouponAdmin(admin.ModelAdmin):
        list_display = ['code', 'valid_from', 'valid_to',

                    'discount', 'active','is_used']

        list_filter = ['active', 'valid_from', 'valid_to']

        search_fields = ['code']



admin.site.register(Product, ProductAdmin) 
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.register(CustomersAddress)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Refunds)


actions = [make_accept_refund]