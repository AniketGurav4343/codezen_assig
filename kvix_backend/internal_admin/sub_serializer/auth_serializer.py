from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser, Group
from rest_framework.authtoken.models import Token
from internal_admin.models import *
from platform_central.models import *

from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
# from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode



class UserLoginSerializer(serializers.ModelSerializer):    

    mobile = serializers.CharField(max_length=10,required=False)
    email = serializers.CharField(required=False)

    class Meta:
        model = AuthUser
        fields = ('mobile', 'password', 'email')


# class UserValidateSerializer(serializers.ModelSerializer):  
    
#     mobile = serializers.CharField(max_length=10)

#     class Meta:
#         model = User
#         fields = "__all__"
#         extra_kwargs = {'mobile': {'required': True}}

class SendOtpSerializer(serializers.ModelSerializer):
    
    mobile = serializers.CharField(required=True)
    otp = serializers.CharField(required=False)
    expiry = serializers.DateTimeField(required=False)
    is_active = serializers.IntegerField(default="1")

    class Meta:
        model = OTP
        fields = ('otp','mobile','expiry','is_active')


class UserGetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email','mobile','dob','role','verified')


class VerifySerializer(serializers.ModelSerializer):
    
	# mobile = serializers.CharField(max_length=10, help_text="Register Mobile Number")

	class Meta:
		model = User
		fields = ("id","mobile","first_name","middle_name","last_name","email",
					"gender","alternate_mobile","dob",
					"age","user")


class ValidateOtpSerializer(serializers.ModelSerializer):
    
    mobile = serializers.CharField(required=True)
    otp = serializers.CharField(required=False)
    expiry = serializers.DateTimeField(required=False)
    is_active = serializers.IntegerField(default="1")

    class Meta:
        model = OTP
        fields = ('otp','mobile','expiry','is_active')


class LogoutSerializer(serializers.Serializer):
    
	class Meta:
		model = Token
		fields = ()


# class ChangePasswordSerializer(serializers.ModelSerializer):
    
#     old_password = serializers.CharField(max_length=20, help_text="Old Password")
#     new_password = serializers.CharField(max_length=20, help_text="New Password")
#     retype_password = serializers.CharField(max_length=20, help_text="Re-Type Password")

#     class Meta:
#         model = User
#         fields = ('old_password', 'new_password', 'retype_password')
#         # extra_kwargs = {'mobile': {'required': True}}


# class ForgotPasswordSerializer(serializers.ModelSerializer):
    
# 	email = serializers.CharField(max_length=255, help_text="Registered Email",required=False)
# 	otp = serializers.CharField(max_length=6, help_text="OTP send to Your mobile",required=False)
# 	new_password = serializers.CharField(max_length=20, help_text="New Password",required=False)
# 	retype_password = serializers.CharField(max_length=20, help_text="Re-Type Password",required=False)

# 	class Meta:
# 		model = User
# 		fields = ('email', 'otp', 'new_password', 'retype_password')


# class ResetPasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True,help_text="old password")
#     new_password = serializers.CharField(required=True,help_text="new password")
#     retype_password = serializers.CharField(required=True,help_text="Re-Type password")


# class SetNewPasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(
#         min_length=6, max_length=68, write_only=True)
#     token = serializers.CharField(
#         min_length=1, write_only=True)
#     uidb64 = serializers.CharField(
#         min_length=1, write_only=True)

#     class Meta:
#         fields = ['password', 'token', 'uidb64']

#     def validate(self, attrs):
#         try:
#             password = attrs.get('password')
#             token = attrs.get('token')
#             uidb64 = attrs.get('uidb64')

#             id = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise AuthenticationFailed('The reset link is invalid', 401)

#             user.set_password(password)
#             user.save()

#             return (user)
#         except Exception as e:
#             raise AuthenticationFailed('The reset link is invalid', 401)
#         return super().validate(attrs)