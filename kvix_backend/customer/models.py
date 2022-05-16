from django.db import models
from platform_central.models import *
from distributor.models import *
from django.contrib.auth.models import User as AuthUser

# Create your models here.


class CustomerGlobal(models.Model):

    GENDER_TYPE = (
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other'),
        )
    

    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    gender = models.CharField(choices=GENDER_TYPE,max_length=255, blank=True, null=True)
    address_line_1 = models.TextField(blank=True, null=True, max_length=10000)
    address_line_2 = models.TextField(blank=True, null=True, max_length=10000)
    city = models.CharField(max_length=255,blank=True,null=True)
    state = models.CharField(max_length=255,blank=True,null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    mobile_number = models.CharField(max_length=10, blank=True, null=True)
    alternate_mobile_number = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.pk, self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = "Customer Global"


class CustomerUser(models.Model):

    GENDER_TYPE = (
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other'),
        )

    customer_global = models.ForeignKey(CustomerGlobal, blank=True, null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    gender = models.CharField(choices=GENDER_TYPE,max_length=255, blank=True, null=True)
    address_line_1 = models.TextField(blank=True, null=True, max_length=10000)
    address_line_2 = models.TextField(blank=True, null=True, max_length=10000)
    city = models.CharField(max_length=255,blank=True,null=True)
    state = models.CharField(max_length=255,blank=True,null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    mobile_number = models.CharField(max_length=10, blank=True, null=True)
    alternate_mobile_number = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.pk, self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = "Customer User"

class CustomerDistributorMapping(models.Model):
    
    distributor_firm = models.ForeignKey(DistributorFirm, blank=True, null=True,on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerUser, blank=True, null=True,on_delete=models.CASCADE)
    is_deleted = models.BooleanField(blank=True,null=True,default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.pk) + str(self.distributor_firm) + str(self.customer)

        
    class Meta:
        verbose_name_plural = "Customer Distributor Mapping"       


class CustomerProfilePicture(models.Model):

    customer = models.ForeignKey(CustomerUser, blank=True, null=True,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="customer_images/%Y/%m/%d",blank=True,null=True,help_text="profile image")
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.pk, self.customer)

    class Meta:
        verbose_name_plural = "Customer Profile Picture"


class CustomerApproval(models.Model):

    CUSTOMER_STATUS = (
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
        )

    customer = models.ForeignKey(CustomerUser, blank=True, null=True,on_delete=models.CASCADE)
    customer_status = models.CharField(choices=CUSTOMER_STATUS,max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(AuthUser, blank = True, null = True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.pk, self.customer)

    class Meta:
        verbose_name_plural = "Customer Approval"

class CustomerBankDetail(models.Model):

    PAYMENT_MODE  = (
        ('BANK','BANK'),
        ('UPI','UPI'),
        )

    customer = models.ForeignKey(CustomerUser, blank=True, null=True,on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255, blank=True, null=True) 
    account_number = models.CharField(max_length=255, blank=True, null=True)
    re_enter_account_number = models.CharField(max_length=255, blank=True, null=True)
    payment_mode        = models.CharField(choices=PAYMENT_MODE,max_length=255, blank=True, null=True)
    ifsc_code = models.CharField(max_length=255, blank=True, null=True) 
    branch = models.CharField(max_length=255, blank=True, null=True) 
    account_holder_name = models.CharField(max_length=255, blank=True, null=True)
    primary_upi = models.CharField(max_length=255, blank=True, null=True)
    umrn_number = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(AuthUser, blank = True, null = True, on_delete=models.CASCADE)


    def __str__(self):
        return '{}-{}'.format(self.pk, self.customer)

    class Meta:
        verbose_name_plural = "Customer Bank Detail"

class CustomerKYCDocument(models.Model):

    DOCUMENT_STATUS = (
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
        )


    customer = models.ForeignKey(CustomerUser, blank=True, null=True,on_delete=models.CASCADE)
    document_master = models.ForeignKey(DocumentMaster, blank=True, null=True, on_delete=models.CASCADE)
    document_status = models.CharField(choices=DOCUMENT_STATUS,max_length=255, blank=True, null=True)
    document_file = models.FileField(upload_to='customer_verification_documents/%Y/%m/%d/', blank=True, null=True, help_text="kyc doc")
    document_file_front = models.FileField(upload_to='customer_verification_front_documents/%Y/%m/%d/', blank=True, null=True, help_text="kyc doc - front side")
    document_file_back = models.FileField(upload_to='customer_verification_back_documents/%Y/%m/%d/', blank=True, null=True, help_text="kyc doc - back side")
    is_verified = models.BooleanField(blank=True, null=True, default=False)
    api_response = models.TextField(blank=True,null=True)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.pk, self.customer)

    class Meta:
        verbose_name_plural = "Customer Bank Detail"