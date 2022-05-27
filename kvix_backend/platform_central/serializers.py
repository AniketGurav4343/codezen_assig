from rest_framework import serializers
from platform_central.models import *

class SendOtpSerializer(serializers.ModelSerializer):
    
    mobile = serializers.CharField(required=True)
    otp = serializers.CharField(required=False)
    expiry = serializers.DateTimeField(required=False)
    is_active = serializers.IntegerField(default="1")
    created_at = serializers.DateTimeField(required=False)

    class Meta:
        model = OTP
        fields = ('otp','mobile','expiry','is_active','created_at')