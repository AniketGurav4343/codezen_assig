from django.urls import path, include
from customer.views import *

urlpatterns = [
    path('customer_upload_picture/', CustomerUploadPicture.as_view()),
    path('customer_register/', CustomerRegister.as_view()),
    
]