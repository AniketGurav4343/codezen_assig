from django.contrib import admin
from customer.models import *
# Register your models here.

admin.site.register(CustomerGlobal)
admin.site.register(CustomerUser)
admin.site.register(CustomerProfilePicture)