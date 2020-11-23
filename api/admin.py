from django.contrib import admin

# Register your models here.

from .models import Product, ShoppingCart

admin.site.register(Product)
admin.site.register(ShoppingCart)