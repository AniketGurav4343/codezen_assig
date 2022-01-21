from django.db import models
from django.utils.translation import gettext as _
# Create your models here.
class Product(models.Model):
    product_name = models.CharField(_("product_name"),max_length=100)
    amount = models.FloatField(_("amount"))
