from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display= ['product_name','amount']