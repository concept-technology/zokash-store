from django.contrib import admin
from .models import Product,Cart,Order, Category, BillingAddress
from django.utils.html import format_html

# # Register your models here.

class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:50px; max-height:100px"/>'.format(obj.img_1.url))
    list_display = ['title', 'image_tag', 'price', 'discount_price']
    image_tag.short_description = 'Image'
admin.site.register(Product, ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'get_price_tag']   
admin.site.register(Cart, CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display= [ 'user','number_of_items','total_price','is_ordered',]
    readonly_fields = ('user',)
admin.site.register(Order, OrderAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
admin.site.register(Category, CategoryAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = '__all__'
admin.site.register(BillingAddress)