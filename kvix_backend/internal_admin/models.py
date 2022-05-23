from django.db import models
from platform_central.models import Roles
from django.contrib.auth.models import User as AuthUser

#Create your models here.

class User(models.Model):

    GENDER_TYPE = (
        ('M','M'),
        ('F','F'),
        ('O','O'),
    )

    first_name = models.CharField(max_length=255, blank=True, null=True) 
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    dob = models.DateField(max_length=20, null=True, blank=True)
    verified = models.BooleanField(blank=False, null=False, default=False)
    role = models.ForeignKey(Roles, blank = True, null = True, on_delete=models.CASCADE)
    is_otp_verified = models.BooleanField(blank=True,null=True,default=False)
    is_deleted = models.BooleanField(blank=False, null=False, default=False)
    is_active = models.BooleanField(blank=False, null=False, default=True)
    created_by = models.ForeignKey(AuthUser, blank = True, null = True, on_delete=models.CASCADE)
    user = models.ForeignKey(AuthUser, blank = True, null = True, on_delete=models.CASCADE,related_name="django_user")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.first_name) + str(self.last_name) + str(self.mobile)
        
    class Meta:
        verbose_name_plural = "User"