from django.urls import path
from platform_central.views import *

urlpatterns = [
    path('v1/Send_otp/', SendOTP.as_view()),
]