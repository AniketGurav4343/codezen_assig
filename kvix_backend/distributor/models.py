from django.db import models
from platform_central.models import *
from django.contrib.auth.models import User as AuthUser

# Create your models here.


class DistributorFirm(models.Model):

    firm_name = models.CharField(max_length=255,blank=True,null=True)
    firm_type = models.ForeignKey(FirmType, blank=True, null=True,on_delete=models.CASCADE)
    firm_license_number = models.CharField(max_length=255,blank=True,null=True)
    firm_license_copy   = models.FileField(upload_to='distributorfirm_documents/%Y/%m/%d/', blank=True, null=True, help_text="licence_copy doc")
    created_at        = models.DateTimeField(auto_now_add=True, null=True)
    updated_at        = models.DateTimeField(auto_now=True)
    is_deleted        = models.BooleanField(blank=True, null=True, default=False)
    created_by = models.ForeignKey(AuthUser, blank = True, null = True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.pk, self.firm_name)

    class Meta:
        verbose_name_plural = "Distributor Firm"


class DistributorUser(models.Model):

    distributor_firm = models.ForeignKey(DistributorFirm, blank=True, null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    address_line_1 = models.TextField(blank=True, null=True, max_length=10000)
    address_line_2 = models.TextField(blank=True, null=True, max_length=10000)
    city = models.CharField(max_length=255,blank=True,null=True)
    state = models.CharField(max_length=255,blank=True,null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    mobile_number = models.CharField(max_length=10, blank=True, null=True)
    alternate_mobile_number = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(AuthUser,blank=True,null=True,on_delete=models.CASCADE)
    created_by = models.ForeignKey(AuthUser, blank = True, null = True, on_delete=models.CASCADE, related_name='DistributorUser')
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.pk, self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = "Distributor User"


class DistributorFirmAddresses(models.Model):

    distributor_firm = models.ForeignKey(DistributorFirm, blank=True, null=True,on_delete=models.CASCADE)
    address_line_1 = models.TextField(blank=True, null=True, max_length=10000)
    address_line_2 = models.TextField(blank=True, null=True, max_length=10000)
    city = models.CharField(max_length=255,blank=True,null=True)
    state = models.CharField(max_length=255,blank=True,null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.pk, self.distributor_firm)

    class Meta:
        verbose_name_plural = "Distributor Firm Address"

class DistributorApproval(models.Model):

    DISTRIBUTOR_STATUS = (
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
        )

    distributor_firm = models.ForeignKey(DistributorFirm, blank=True, null=True,on_delete=models.CASCADE)
    distributor_status = models.CharField(choices=DISTRIBUTOR_STATUS,max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(AuthUser, blank = True, null = True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.pk, self.distributor_firm)

    class Meta:
        verbose_name_plural = "Distributor Approval"

class DistributorBankDetail(models.Model):

    distributor_firm = models.ForeignKey(DistributorFirm, blank=True, null=True,on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255, blank=True, null=True) 
    account_number = models.CharField(max_length=255, blank=True, null=True) 
    re_enter_account_number = models.CharField(max_length=255, blank=True, null=True)
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
        return '{}-{}'.format(self.pk, self.distributor_firm)

    class Meta:
        verbose_name_plural = "Distributor Bank Detail"


class DistributorKYCDocument(models.Model):

    DOCUMENT_STATUS = (
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
        )


    distributor_firm = models.ForeignKey(DistributorFirm, blank=True, null=True,on_delete=models.CASCADE)
    distributor_user = models.ForeignKey(DistributorUser, blank=True, null=True,on_delete=models.CASCADE)
    document_master = models.ForeignKey(DocumentMaster, blank=True, null=True, on_delete=models.CASCADE)
    document_status = models.CharField(choices=DOCUMENT_STATUS,max_length=255, blank=True, null=True)
    document_file = models.FileField(upload_to='distributor_verification_documents/%Y/%m/%d/', blank=True, null=True, help_text="kyc doc")
    document_file_front = models.FileField(upload_to='distributor_verification_front_documents/%Y/%m/%d/', blank=True, null=True, help_text="kyc doc - front side")
    document_file_back = models.FileField(upload_to='distributor_verification_back_documents/%Y/%m/%d/', blank=True, null=True, help_text="kyc doc - back side")
    is_verified = models.BooleanField(blank=True, null=True, default=False)
    api_response = models.TextField(blank=True,null=True)
    is_deleted = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.pk, self.distributor_firm)

    class Meta:
        verbose_name_plural = "Distributor KYC Document"