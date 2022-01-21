from rest_framework import serializers
from rest_framework import fields
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, value):
        d = Product.objects.filter(name=value).exists()
        if d == True:
            raise serializers.ValidationError("Product Name Is All Ready Exist")


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'



class OrdersCustomerSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(source="Customer")
    class Meta:
        model = Orders
        fields = '__all__'
        

class OrdProPrefetchSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(many=True)
    class Meta:
        model = Orders
        fields = '__all__'