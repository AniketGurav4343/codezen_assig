from curses.ascii import US

from django.conf import settings
import datetime
import json
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse
import pytz

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from common import messages

from django.contrib.auth import login as django_login

from rest_framework.response import Response
from rest_framework import status

from platform_central.models import Token as LogToken

from platform_central.helpers.validation_helper import email_mobile_validator
from internal_admin.sub_serializer.auth_serializer import UserLoginSerializer, LogoutSerializer

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
# from miscellaneous.api_function_helpers.email_helper import send_emailer, otp_verification

from internal_admin.api_function_helpers.otp_helper import *

from django.db.models import Q

from django.contrib.auth.models import User

import requests


def login_request(request):
        mobile = request.data['mobile']
        response = {}

        if (not mobile):
            return Response({
                            "success" : False,
                            "status_code" :status.HTTP_200_OK,
                            "message" : messages.AUTHENTICATION_INVALID,
                            "data" : None},
                            status=status.HTTP_200_OK
                            )


        mobile_valid = email_mobile_validator(mobile=mobile)

        if mobile_valid is None:
            return Response({
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': messages.MOBdILE_INVALID,
                    'data':None},
                    status = status.HTTP_400_BAD_REQUEST)

        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():

            if not User.objects.filter(
                mobile = serializer.data['mobile']).exists():
                return Response({
                            "success" : False,
                            "status_code" :status.HTTP_200_OK,
                            "message" : messages.MOBILE_NOT_FOUND,
                            "data" : None},
                            status=status.HTTP_200_OK
                            )
            else:
                platform_user = User.objects.get(
                    mobile = serializer.data["mobile"])

            user = User.objects.get(username=platform_user.mobile)

            if user is not None and user.is_active:
                django_login(request, user)

                data = {}
                

                #delete all previous token 
                LogToken.objects.filter(user=user).delete()


                token = LogToken.objects.create(user=user)

                ############################# PERMISSIONS ##################################
                # permissions_slug_list =  fetch_permissions(
                #     request,mobile = platform_user.mobile)


                data["token"] = token.key
                # data["permissions_slug_list"] = permissions_slug_list

                
                response["data"] = data
                
                return Response({
                        "success" : True,
                        "status_code" :status.HTTP_200_OK,
                        "message" : messages.LOGIN_SUCCESSFULL,
                        "data" : response},
                        status=status.HTTP_200_OK
                        )

            else:
            
                return Response({
                            "success" : False,
                            "status_code" :status.HTTP_200_OK,
                            "message" : "User Not Found",
                            "data" : None},
                            status=status.HTTP_200_OK
                            ) 
        else:
            return Response({
                        "success" : False,
                        "status_code" :status.HTTP_400_BAD_REQUEST,
                        "message" : "cant login",
                        "data" : None},
                        status=status.HTTP_400_BAD_REQUEST
                        )  


def logout_user(self, request, format=None):

        serializer = LogoutSerializer(data = request.data)
        response = {}

        try:
            key=request.META['HTTP_AUTHORIZATION'].split(' ')[1].strip()
        except KeyError:

            return Response({
                            "success" : False,
                            "status_code" :status.HTTP_200_OK,
                            "message" : "Unable to get Token in Header",
                            "data" : None},
                            status=status.HTTP_200_OK
            )
            
        if not LogToken.objects.filter(key = key).exists():

            return Response({
                            "success" : False,
                            "status_code" :status.HTTP_200_OK,
                            "message" : "Token not sent OR Token is Incorrect",
                            "data" : None},
                            status=status.HTTP_200_OK
            )
        else:
            LogToken.objects.get(key = key).delete()
            return Response({
                            "success" : True,
                            "status_code" :status.HTTP_200_OK,
                            "message" : "Cya !! You've Been Logged Out",
                            "data" : None},
                            status=status.HTTP_200_OK
            )

# def change_password(self, request, format=None):
    
#     try: 

#         user_obj = User.objects.get(id=request.user.id)

#         request.data["mobile"] = user_obj.username
        
#         serializer = ChangePasswordSerializer(data = request.data)
#         if serializer.is_valid():
            
#             if serializer.data['new_password'] != serializer.data[
#                                             'retype_password']:

#                 return Response({
#                             "success" : False,
#                             "status_code" :status.HTTP_200_OK,
#                             "message" : messages.PASSWORD_DO_NOT_MATCH,
#                             "data" : None},
#                             status=status.HTTP_200_OK
#                             )

#             user = authenticate(
#                     username = user_obj.username, 
#                     password = serializer.data["old_password"]
#                     )


#             if user is not None and user.is_active:

#                 if User.objects.filter(password=user.password,
#                                             username = user).exists():

#                     auth_user = User.objects.get(
#                                             password = user.password, 
#                                             username = user)    
                        
#                     if serializer.data[
#                             'new_password'] == serializer.data[
#                                             'retype_password']:

#                         new_pass = make_password(serializer.data[
#                                                 'new_password'])

#                         auth_user.password
#                         auth_user.save()
#                         # auth_user.save()

#                         user_obj.set_password(
#                                     serializer.data['new_password'])
#                         user_obj.save()

#                         admin_user = AdminUser.objects.filter(user=user_obj)

#                         if admin_user.exists():
#                             admin_user = admin_user.first()
#                             admin_user.password = encrypt(serializer.data["new_password"])
#                             admin_user.save()

#                         return Response({
#                             "success" : True,
#                             "status_code" :status.HTTP_200_OK,
#                             "message" : "Your password has been saved successfully",
#                             "data" : None},
#                             status=status.HTTP_200_OK
#                             )
#                     else :
                        
#                         return Response({
#                             "success" : False,
#                             "status_code" :status.HTTP_200_OK,
#                             "message" : "New Password and Re-enter New Password are not same",
#                             "data" : None},
#                             status=status.HTTP_200_OK
#                         )
#                 else :

#                     return Response({
#                             "success" : False,
#                             "status_code" :status.HTTP_200_OK,
#                             "message" : "You have enter wrong old password",
#                             "data" : None},
#                             status=status.HTTP_200_OK
#                         )
#             else :
#                 return Response({
#                             "success" : False,
#                             "status_code" :status.HTTP_200_OK,
#                             "message" : "Old Password Entered is Wrong",
#                             "data" : None},
#                             status=status.HTTP_200_OK
#                         )
#         else:
#             return Response({
#                             "success" : False,
#                             "status_code" :status.HTTP_200_OK,
#                             "message" : serializer.errors,
#                             "data" : None},
#                             status=status.HTTP_200_OK
#                         )
#     except NameError as e:
#         logger.error('CHANGE PASSWORD HELPER : {}'.format( e))
#         raise ce.NameErrorCe

#     except AttributeError as e:
#         logger.error('CHANGE PASSWORD HELPER : {}'.format( e))
#         raise ce.AttributeErrorCe

#     except KeyError as e:
#         logger.error('CHANGE PASSWORD HELPER : {}'.format( e))
#         raise ce.KeyErrorCe

#     except UnboundLocalError as e:
#         logger.error('CHANGE PASSWORD HELPER : {}'.format( e))
#         raise ce.UnknownColumnErrorCe

#     except Exception as e:
#         logger.error('CHANGE PASSWORD HELPER : {}'.format( e))
#         raise ce.InternalServerError


# def change_password_by_admin(self, request, format=None):
    
#     try:
#         serializer = ChangePasswordAdminSerializer(data = request.data)
#         if serializer.is_valid():
            
#             admin_user = serializer.validated_data["id"]

#             if serializer.validated_data['new_password'] != serializer.validated_data['retype_password']:

#                 return Response({
#                             "success" : False,
#                             "status_code" :status.HTTP_200_OK,
#                             "message" : messages.PASSWORD_DO_NOT_MATCH,
#                             "data" : None},
#                             status=status.HTTP_200_OK
#                             )


#             if admin_user.user is not None:
#                 django_user = admin_user.user
#                 django_user.set_password(serializer.validated_data["new_password"])
#                 django_user.save()
#                 admin_user.password = encrypt(serializer.validated_data["new_password"])
#                 admin_user.save()
                
#             return Response({
#                 "success" : True,
#                 "status_code" :status.HTTP_200_OK,
#                 "message" : "Password has been updated successfully",
#                 "data" : None},
#                 status=status.HTTP_200_OK
#                 )

#         else:
#             return Response({
#                             "success" : False,
#                             "status_code" :status.HTTP_200_OK,
#                             "message" : handle_errors(serializer.errors),
#                             "data" : None},
#                             status=status.HTTP_200_OK
#                         )
#     except NameError as e:
#         logger.error('CHANGE PASSWORD HELPER : {}'.format( e))
#         raise ce.NameErrorCe

#     except AttributeError as e:
#         logger.error('CHANGE PASSWORD HELPER : {}'.format( e))
#         raise ce.AttributeErrorCe

#     except KeyError as e:
#         logger.error('CHANGE PASSWORD HELPER : {}'.format( e))
#         raise ce.KeyErrorCe

#     except UnboundLocalError as e:
#         logger.error('CHANGE PASSWORD HELPER : {}'.format( e))
#         raise ce.UnknownColumnErrorCe

#     except Exception as e:
#         logger.error('CHANGE PASSWORD HELPER : {}'.format( e))
#         raise ce.InternalServerError


# def forgot_password(self, request, format=None):
#     try:
#         serializer = self.serializer_class(data=request.data)
#         response = {}
#         responsedata = []
#         if serializer.is_valid():

#             # Check for Email address or phone number and get user obj
            
#             user_obj = AdminUser.objects.filter(Q(
#                 email=serializer.validated_data['email'], is_deleted=False
#                 ) | Q(
#                     mobile=serializer.validated_data['email'], 
#                     is_deleted=False))

#             if user_obj.exists():
#                 user_obj = user_obj.last()
#                 django_user_obj = user_obj.user
#             else:

#                 return Response({
#                     'success': False,
#                     'status_code': status.HTTP_200_OK,
#                     'message':"This email address or mobile number is not registered in this domain",
#                     'data':None},
#                     status = status.HTTP_200_OK)

#             mobile_verification_token = OtpModel.objects.create(mobile=user_obj.mobile)

#             message = 'Verification Link Has Been Send on registered Mobile Number and Email address'

#             # Email And Message Body
#             email_body  = "Hi {1}, Your OTP for setting new password is {0}".format(mobile_verification_token.otp, user_obj.first_name)
            

#             request.data["body_text"] = email_body
#             request.data["recipient"] = user_obj.email
#             request.data["subject"] = "Forgot Password OTP"
            
#             # send_emailer(self, request)
#             otp_verification(user_obj.first_name, mobile_verification_token.otp, user_obj.email)
            

#             #Send OTP  (Has to work)

#             #Sending Response
#             return Response({
#                     'success': True,
#                     'status_code': status.HTTP_200_OK,
#                     'message': "Forgot Password Link Send",
#                     'data':None},
#                     status = status.HTTP_200_OK)
        
#         # Serializer Error
#         else:
#             return Response({
#                     'success': False,
#                     'status_code': status.HTTP_400_BAD_REQUEST,
#                     'message': handle_errors(serializer.errors),
#                     'data':None},
#                     status = status.HTTP_400_BAD_REQUEST)
        
#     except NameError as e:
#         logger.error('FORGOT PASSWORD HELPER : {}'.format( e))
#         raise ce.NameErrorCe

#     except AttributeError as e:
#         logger.error('FORGOT PASSWORD HELPER : {}'.format( e))
#         raise ce.AttributeErrorCe

#     except KeyError as e:
#         logger.error('FORGOT PASSWORD HELPER : {}'.format( e))
#         raise ce.KeyErrorCe

#     except UnboundLocalError as e:
#         logger.error('FORGOT PASSWORD HELPER : {}'.format( e))
#         raise ce.UnknownColumnErrorCe

#     except Exception as e:
#         logger.error('FORGOT PASSWORD HELPER : {}'.format( e))
#         raise ce.InternalServerError


# def reset_password(self,request):
#     try:
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():

#             current_user = request.user
#             matchcheck= check_password(serializer.validated_data["old_password"], current_user.password)

#             if matchcheck:
#                 if serializer.validated_data["new_password"] == serializer.validated_data["retype_password"]:
#                     current_user.set_password(serializer.validated_data["new_password"])
#                     current_user.save()
#                     return Response({
#                                 'success': False,
#                                 'status_code': status.HTTP_200_OK,
#                                 'message': messages.PASSWORD_RESET_SUCCESS,
#                                 'data':None},
#                                 status = status.HTTP_200_OK)
#                 else:
#                     return Response({
#                             'success': False,
#                             'status_code': status.HTTP_200_OK,
#                             'message': messages.PASSWORD_DO_NOT_MATCH,
#                             'data':None},
#                             status = status.HTTP_200_OK)
#             else:
#                 return Response({
#                         'success': False,
#                         'status_code': status.HTTP_200_OK,
#                         'message': "You have enter wrong old password",
#                         'data':None},
#                         status = status.HTTP_200_OK)
#         else:
#             return Response({
#                     'success': False,
#                     'status_code': status.HTTP_400_BAD_REQUEST,
#                     'message': handle_errors(serializer.errors),
#                     'data':None},
#                     status = status.HTTP_400_BAD_REQUEST)
#     except NameError as e:
#         logger.error('RESET PASSWORD HELPER : {}'.format( e))
#         raise ce.NameErrorCe

#     except AttributeError as e:
#         logger.error('RESET PASSWORD HELPER : {}'.format( e))
#         raise ce.AttributeErrorCe

#     except KeyError as e:
#         logger.error('RESET PASSWORD HELPER : {}'.format( e))
#         raise ce.KeyErrorCe

#     except UnboundLocalError as e:
#         logger.error('RESET PASSWORD HELPER : {}'.format( e))
#         raise ce.UnknownColumnErrorCe

#     except Exception as e:
#         logger.error('RESET PASSWORD HELPER : {}'.format( e))
#         raise ce.InternalServerError


# def validate_forgot_password(self,request):

#     # try:

#     now = datetime.datetime.now()
#     datetime_object = now.strftime('%Y-%m-%d %H:%M:%S')


#     response = {}
#     responsedata = []

#     serializer = self.serializer_class(data=request.data)
#     if serializer.is_valid():

#         user_obj = AdminUser.objects.filter(Q(
#             email=serializer.validated_data['email'], is_deleted=False
#             ) | Q(
#                 mobile=serializer.validated_data['email'], 
#                 is_deleted=False))

#         if user_obj.exists():
#             user_obj = user_obj.last()
#             django_user_obj = user_obj.user

#             if not django_user_obj:
#                 return Response({
#                     'success': False,
#                     'status_code': status.HTTP_200_OK,
#                     'message':messages.USER_FOUND_BUT_NO_DJANGO_USER,
#                     'data':None},
#                     status = status.HTTP_200_OK)


#         else:

#             return Response({
#                 'success': False,
#                 'status_code': status.HTTP_200_OK,
#                 'message':"This email address or mobile number is not registered in this domain",
#                 'data':None},
#                 status = status.HTTP_200_OK)

        
#         if serializer.validated_data['new_password'] != serializer.validated_data[
#                                         'retype_password']:

#             return Response({
#                         "success" : False,
#                         "status_code" :status.HTTP_200_OK,
#                         "message" : messages.PASSWORD_DO_NOT_MATCH,
#                         "data" : None},
#                         status=status.HTTP_200_OK
#                         )


#         res = OtpModel.objects.filter(
#             mobile=user_obj.mobile,
#             is_active=1).last()

#         if res:     
#             latest_otp = res.otp

#             if latest_otp is None:
#                     return Response({
#                     'success': False,
#                     'status_code': status.HTTP_200_OK,
#                     'message': messages.OTP_NOT_FOUND,
#                     'data':None},
#                     status = status.HTTP_200_OK)
#             else:
#                 expiry_timestamp = res.expiry
#                 expiry_obj = expiry_timestamp.strftime("%Y-%m-%d %H:%M:%S")                    

#                 if settings.SMS_SERVICE_STATUS:
#                     if latest_otp == serializer.validated_data[
#                     "otp"]:
#                         if datetime_object < expiry_obj:
#                             return Response({
#                                 'success': False,
#                                 'status_code': status.HTTP_200_OK,
#                                 'message': messages.OTP_EXPIRED,
#                                 'data':None},
#                                 status = status.HTTP_200_OK)    
#                     else:
#                         return Response({
#                             'success': False,
#                             'status_code': status.HTTP_400_BAD_REQUEST,
#                             'message': messages.INVALID_OTP,
#                             'data':None},
#                             status = status.HTTP_400_BAD_REQUEST)
                        
#                 else:
#                     if not serializer.validated_data["otp"]==latest_otp:

#                         return Response({
#                             'success': False,
#                             'status_code': status.HTTP_400_BAD_REQUEST,
#                             'message': messages.INVALID_OTP,
#                             'data':None},
#                             status = status.HTTP_400_BAD_REQUEST)


#                 res.is_active = 0
#                 res.save()     


#                 # Change Password
#                 django_user_obj.set_password(serializer.validated_data['new_password'])
#                 django_user_obj.save()

#                 return Response({
#                     'success': True,
#                     'status_code': status.HTTP_200_OK,
#                     'message': messages.PASSWORD_CHANGED,
#                     'data':None},
#                     status = status.HTTP_200_OK
#                 )
#         else:
#             return Response({
#                 'success': False,
#                 'status_code': status.HTTP_400_BAD_REQUEST,
#                 'message': messages.OTP_NOT_FOUND_ERROR,
#                 'data':None},
#                 status = status.HTTP_400_BAD_REQUEST)

    

#     # Serializer Error
#     else:
#         return Response({
#                 'success': False,
#                 'status_code': status.HTTP_400_BAD_REQUEST,
#                 'message': handle_errors(serializer.errors),
#                 'data':None},
#                 status = status.HTTP_400_BAD_REQUEST)

