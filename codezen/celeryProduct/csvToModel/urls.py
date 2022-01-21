from django.urls import path,include
from . import views
urlpatterns = [
    path('Product_pd_view', views.Product_view, name='Product_pd_view'),
]