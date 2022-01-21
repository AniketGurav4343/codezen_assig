from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()

class Customer(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    user=models.ForeignKey(User,on_delete=CASCADE,related_name='Customer')


class Seller(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    user=models.ForeignKey(User,on_delete=CASCADE,related_name='Seller')

class Orders(models.Model):
    Customer=models.ForeignKey(Customer,on_delete=CASCADE,related_name='Orders')
    Seller=models.ForeignKey(Seller,on_delete=CASCADE,related_name='Orders')
    products = models.ManyToManyField(Product)
    amount = models.IntegerField()

class PlatformApiCall(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE,related_name='PlatformApiCall')
    requested_url = models.CharField(max_length=500,null=True)
    requested_data = models.CharField(max_length=500,null=True)
    response_data = models.CharField(max_length=500,null=True)

