import datetime
import random
import binascii
import os
from django.db import models
from django.contrib.auth.models import User
from six import python_2_unicode_compatible
from django.utils.translation import gettext_lazy as _
import rest_framework.authtoken.models
from django.contrib.auth.models import User as AuthUser


# Create your models here.


class PlatformApiCall(models.Model):
    """ Info about API requested by user """
    user              = models.ForeignKey(AuthUser, blank=True, null=True, on_delete=models.CASCADE)
    requested_url     = models.CharField(max_length=250, null=True, verbose_name='requested url')
    requested_data    = models.TextField(verbose_name='requested data')
    response_data     = models.TextField(verbose_name='response data')
    client_ip_address = models.CharField(max_length=200, null=True, blank=True)
    created_at        = models.DateTimeField(auto_now_add=True, null=True)
    updated_at        = models.DateTimeField(auto_now=True)
    is_deleted        = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return '{}-{}'.format(self.pk,self.requested_url)

    class Meta:
        verbose_name_plural = 'Platform API Calls'
        db_table = 'platform_api_call'



@python_2_unicode_compatible
class Token(rest_framework.authtoken.models.Token):
    # key is no longer primary key, but still indexed and unique
    key  = models.CharField(_("Key"), max_length=40, blank=True, db_index=True, unique=True)
    # relation to user is a ForeignKey, so each user can have more than one token
    user = models.ForeignKey(User, related_name='auth_tokens', on_delete=models.CASCADE, verbose_name=_("User"))
    name = models.CharField(_("Name"), max_length=64, blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)    
    # If you have multiple tokens, you might want to have a way to manage them. That usually means referring to tokens by a URL. As the key is supposed to be secret, it should not appear in URLs, because URLs usually end up in a kind of places, e.g. server logs.
    # Tokens now have a name to be able to differentiate them. The name should be unique per user    
     
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)  

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()    

    class Meta:
        # unique_together = (('user', 'name'),)
        verbose_name_plural = 'Tokens'
        db_table            = 'rest_framework_authtoken_model_token'


class OTP(models.Model):

    otp = models.CharField(max_length=100,unique=True, null=False, blank=False)
    mobile = models.CharField(max_length=11,unique=False, null=True, blank=True)
    email = models.CharField(max_length=255,blank=True,null=True)
    expiry = models.DateTimeField(blank=False, null=False)
    is_active = models.BooleanField(blank=False, null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    

    def __str__(self):
        return '{}-{}'.format(self.pk,self.otp)
        
    class Meta:
        verbose_name_plural = "OTP"

    def save(self, *args, **kwargs):
        self.otp = random.randint(1000, 9999)
        self.expiry = (datetime.datetime.now() + datetime.timedelta(minutes= 5))
        super(OTP, self).save(*args, **kwargs)



class Roles(models.Model):
   
    role_name = models.SlugField(unique=True, max_length=255)
    role_status = models.IntegerField()
    created_at        = models.DateTimeField(auto_now_add=True, null=True)
    updated_at        = models.DateTimeField(auto_now=True)
    is_deleted        = models.BooleanField(blank=False, null=False, default=False)
    
    class Meta:
        verbose_name_plural = "System Roles"

    def __str__(self):
        return "{}-{}".format(self.pk, self.role_name)



class FirmType(models.Model):
    
    firm_type = models.CharField(max_length=255, blank=False, null=False)
    priority = models.FloatField(null=True, blank=True)
    created_at        = models.DateTimeField(auto_now_add=True, null=True)
    updated_at        = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        verbose_name_plural = "Firm types"
    
    def __str__(self):
        return "{} - {}".format(self.pk,self.firm_type)



class AttemptsChecker(models.Model):

    otp = models.ForeignKey(OTP, on_delete=models.CASCADE,null=True, blank=True)
    attempts_left = models.CharField(max_length=4, null=True, blank=True, default=3)
    retry_after_timestamp = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    is_success = models.IntegerField(null=False, blank=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

# class State(models.Model):
#     name = models.CharField(max_length=255,blank=False,null=False)
#     abbreviation = models.CharField(max_length=2, blank=True,null=True)
#     created_at        = models.DateTimeField(auto_now_add=True, null=True)
#     updated_at        = models.DateTimeField(auto_now=True)
#     is_deleted        = models.BooleanField(blank=False, null=False, default=False)

#     class Meta:
#         verbose_name_plural = "States"
    
#     def __str__(self):
#         return "{} - {} - {}".format(self.pk,self.name,self.abbreviation)



# class City(models.Model):
#     name = models.CharField(max_length=255,blank=False,null=False)
#     created_at        = models.DateTimeField(auto_now_add=True, null=True)
#     updated_at        = models.DateTimeField(auto_now=True)
#     is_deleted        = models.BooleanField(blank=False, null=False, default=False)

#     class Meta:
#         verbose_name_plural = "Cities"
    
#     def __str__(self):
#         return "{} - {}".format(self.pk,self.name)



# class PincodeMaster(models.Model):

#     pincode = models.IntegerField(null=False, blank=False)
#     is_deleted = models.BooleanField(blank=False, null=False, default=False)
#     created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_deleted        = models.BooleanField(blank=False, null=False, default=False)

#     def __str__(self):
#         return '{}-{}'.format(self.pk,self.pincode)

#     class Meta:
#         verbose_name_plural = "PincodeMaster"



class DocumentMaster(models.Model):

    # DOCUMENT_TYPE = (
    #     ('Nationality Proof','Nationality Proof'),
    #     ('Identity Proof','Identity Proof'),
    #     ('Address Proof','Address Proof'),
    #     ('Income Proof','Income Proof'),
    #     )


    DOCUMENT_CHECK_TYPE = (
        ('Mandatory','Mandatory'),
        ('Optional','Optional')
    )

    DOCUMENT_ACCEPT_TYPE = (
        ('Front','Front'),
        ('Back','Back'),
        ('Both','Both'),
    )

    name = models.CharField(max_length=255, blank=False, null=False) 
    # document_type = models.CharField(choices=DOCUMENT_TYPE,max_length=255, blank=False, null=False) 
    document_check_type = models.CharField(choices=DOCUMENT_CHECK_TYPE,max_length=255, blank=False, null=False)
    document_accept_type = models.CharField(choices=DOCUMENT_ACCEPT_TYPE,max_length=255, blank=False, null=DOCUMENT_ACCEPT_TYPE[0][0])
    require_front_back = models.BooleanField(blank=True,null=True,default=False)
    is_deleted = models.BooleanField(blank=False, null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.pk,self.name)

    class Meta:
        verbose_name_plural = "Document Master"