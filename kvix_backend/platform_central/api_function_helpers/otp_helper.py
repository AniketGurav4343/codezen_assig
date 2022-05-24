from lib2to3.pgen2 import token
import re
from django.conf import settings
import datetime
import hashlib
import logging
import json
import pytz
import random


from datetime import date

from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login

from common import messages
# from utils.api_error_handler import handle_errors
from rest_framework.response import Response
from rest_framework import serializers, status

from platform_central.models import OTP as OtpModel,AttemptsChecker
# from internal_admin.api_function_helpers.login_helper import validate_request
from platform_central.api_function_helpers.sms_helper import *
from internal_admin.models import User
from django.contrib.auth.models import User
from platform_central.models import Token as LogToken
# from miscellaneous.api_function_helpers.email_helper impormodelst send_emailer, otp_verification
from internal_admin.sub_serializer.auth_serializer import VerifySerializer

from platform_central.models import OTP
from datetime import timedelta
from django.utils import timezone

def send_otp(self, request, format=None):
    return Response({
                        'success': False,
                        'status_code': status.HTTP_200_OK,
                        'message': "success",
                        'data':'123456'},
                        status = status.HTTP_200_OK
                    )
# def send_otp(self, request, format=None):
#     """
#     Helper funtion to send OTP

#     """
#     serializer = self.serializer_class(data=request.data)

#     if serializer.is_valid():

#         user_mobile = request.data.get('mobile')
#         user_otp = OTP.objects.filter(mobile=user_mobile).last()

#         # otp logic 
#         if user_otp:
#             now = timezone.now()
#             duration = now - user_otp.created_at

#             if duration < timedelta(seconds=30):
#                 return Response({
#                         'success': False,
#                         'status_code': status.HTTP_200_OK,
#                         'message': "OTP Already Sent!, Please try again in 30 sec",
#                         'data':None},
#                         status = status.HTTP_200_OK
#                     )

#         serializer.save()

#         otp_code = serializer.data["otp"]
#         mobile = serializer.data["mobile"]
#         message_hash = serializer.data['message_hash']

#         if settings.SMS_SERVICE_STATUS:

#             # Email And Message Body
#             # message = "{} is the one time password (OTP) for your mobile number verification with FatakPay. Kindly note that the OTP is valid only for 30 minutes. Please do not share this OTP with anyone for security reasons.- FatakPay".format(otp_code) 

#             message = "{} is the one time password (OTP) for your mobile number verification with FatakPay. Kindly note that the OTP is valid only for 30 minutes. Please do not share this OTP with anyone for security reasons.- FatakPay #{}".format(otp_code, message_hash)

#             # r = sendGupShupSMS(message, mobile)

#             # if r.status_code == 200:

#                 # return Response({
#                 #     'success': True,
#                 #     'status_code': status.HTTP_200_OK,
#                 #     'message': messages.OTP_SENT,
#                 #     'data':None},
#                 #     status = status.HTTP_200_OK
#                 # )
#             # else:
#             return Response({
#                 'success': False,
#                 'status_code': status.HTTP_200_OK,
#                 'message': messages.MESSAGE_SERVICE_DOWN,
#                 'data':None},
#                 status = status.HTTP_200_OK
#             )
#         else:
#             if "email_notify" in request.data and request.data["email_notify"]=="yes":

#                 email_body  = "Hi, Your OTP foOTPr is {}".format(otp_code)
                

#                 request.data["body_text"] = email_body
#                 request.data["recipient"] = request.data["email"]
#                 request.data["subject"] = "OTP"
                    

#                 send_emailer(self, request)

#             return Response({
#                 'success': True,
#                 'status_code': status.HTTP_200_OK,
#                 'message': messages.DUMMY_OTP,
#                 'data':None},
#                 status = status.HTTP_200_OK
#             )
        
#     else:
#         return Response({
#                 'success': False,
#                 'status_code': status.HTTP_400_BAD_REQUEST,
#                 'message': handle_errors(serializer.errors),
#                 'data':None},
#                 status = status.HTTP_400_BAD_REQUEST)






def validate_otp(self, request, format=None):
    """
    Helper function to validate OTP and Mobile
    """
           # Creating a datetime object
    now = datetime.datetime.now()
    datetime_object = now.strftime('%Y-%m-%d %H:%M:%S')
    details = request.data
    serializer = self.serializer_class(data=details)

    if serializer.is_valid():
        
        # Get the latest active OTP from DB
        res = OtpModel.objects.filter(
            mobile=serializer.validated_data["mobile"],
            is_active=1).last()

        if res:     
            latest_otp = res.otp

            if latest_otp is None:
                    return Response({
                    'success': False,
                    'status_code': status.HTTP_200_OK,
                    'message': messages.OTP_NOT_FOUND,
                    'data':None},
                    status = status.HTTP_200_OK)
            else:
                expiry_timestamp = res.expiry
                expiry_obj = expiry_timestamp.strftime("%Y-%m-%d %H:%M:%S")                    

                if settings.SMS_SERVICE_STATUS:
                    if latest_otp == serializer.validated_data[
                    "otp"]:
                        if datetime_object < expiry_obj:
                            return Response({
                                'success': False,
                                'status_code': status.HTTP_200_OK,
                                'message': messages.OTP_EXPIRED,
                                'data':None},
                                status = status.HTTP_200_OK)    
                    else:
                        
                        attempts =  AttemptsChecker.objects.filter(
                            otp=res, is_success=0
                        )

                        if attempts.exists():

                            obj = attempts.first()

                            if int(obj.attempts_left) < 1:
                                return Response({
                                'success': False,
                                'status_code': status.HTTP_400_BAD_REQUEST,
                                'message': messages.ATTEMPTS_EXHAUSTED,
                                'data':None},
                                status = status.HTTP_400_BAD_REQUEST)

                            obj.attempts_left = int(obj.attempts_left) -1

                            if obj.attempts_left == 0:
                                obj.retry_after_timestamp = datetime.datetime.now() + datetime.timedelta(minutes=15)

                            obj.save()
                        else:

                            n = 3

                            payload = {
                                "otp" : res,
                                "attempts_left" : n-1
                            }

                            if payload["attempts_left"] == 0:
                                payload["retry_after_timestamp"] = datetime.datetime.now() + datetime.timedelta(minutes=15)
                            AttemptsChecker.objects.create(**payload)


                        return Response({
                            'success': False,
                            'status_code': status.HTTP_400_BAD_REQUEST,
                            'message': messages.INVALID_OTP,
                            'data':None},
                            status = status.HTTP_400_BAD_REQUEST)
                        
                else:
                    if latest_otp == serializer.validated_data["otp"]:

                        res.is_active = 0
                        res.save()    

                        attempts =  AttemptsChecker.objects.filter(
                                    otp=res,is_success=0
                                )

                        if attempts.exists():

                            obj = attempts.first()
                            obj.is_success = 1
                            obj.save() 

                        response = {}

                    else:

                        attempts =  AttemptsChecker.objects.filter(
                            otp=res,is_success=0
                        )

                        if attempts.exists():

                            obj = attempts.first()
                            
                            now = datetime.datetime.now()

                            if obj.retry_after_timestamp is not None and now < obj.retry_after_timestamp:

                                # return Response("bhai thoda badme try kar")  

                                return Response({
                                    'success': False,
                                    'status_code': status.HTTP_400_BAD_REQUEST,
                                    'message': messages.ATTEMPTS_EXHAUSTED_RETRY,
                                    'data':None},
                                    status = status.HTTP_400_BAD_REQUEST)


                            obj.attempts_left = int(obj.attempts_left) -1
                            obj.save()

                            if int(obj.attempts_left) < 1:
                                obj.retry_after_timestamp = datetime.datetime.now() + datetime.timedelta(minutes=15)
                                obj.attempts_left = 3
                                obj.save()

                                return Response({
                                    'success': False,
                                    'status_code': status.HTTP_400_BAD_REQUEST,
                                    'message': messages.ATTEMPTS_EXHAUSTED,
                                    'data':None},
                                    status = status.HTTP_400_BAD_REQUEST)

                            
                        else:

                            n = 3

                            payload = {
                                "otp" : res,
                                "attempts_left" : n-1
                            }
                            create_obj = AttemptsChecker.objects.create(**payload)

                            obj = AttemptsChecker.objects.get(otp=res,is_success=0)

                            if obj.attempts_left <= "0":
                                obj.retry_after_timestamp = datetime.datetime.now() + datetime.timedelta(minutes=15)
                                obj.save()

                        return Response({
                            'success': False,
                            'status_code': status.HTTP_400_BAD_REQUEST,
                            'message': messages.INVALID_OTP.format(obj.attempts_left),
                            'data':None},
                            status = status.HTTP_400_BAD_REQUEST)


                # res.is_active = 0
                # res.save()    

                # attempts =  AttemptsChecker.objects.filter(
                #             otp=res,is_success=0
                #         )

                # if attempts.exists():

                #     obj = attempts.first()
                #     obj.is_success = 1
                #     obj.save() 

                # response = {}

                # validate_request(self, request)

                user = AppUser.objects.filter(
                    mobile=serializer.validated_data["mobile"]).order_by(
                        '-id'
                    ).first()


                app_user = AppUser.objects.filter(user=user.user)
                
                if not app_user.exists():
                    return Response({
                            'success': False,
                            'status_code': status.HTTP_200_OK,
                            'message': messages.APPUSER_NOT_FOUND,
                            'data':None},
                            status = status.HTTP_200_OK)


                app_user = app_user.order_by('-id').first()

                if "new_mobile" in request.data:

                    new_mobile_obj = AppUser.objects.filter(
                        mobile=request.data['new_mobile']
                    )

                    if new_mobile_obj.exists():
                        return Response({
                            'success': False,
                            'status_code': status.HTTP_200_OK,
                            'message': messages.APP_USER_WITH_SIMILAR_MOBILE_EXISTS.format(request.data['new_mobile']),
                            'data':None},
                            status = status.HTTP_200_OK)
                    else:
                        app_user.new_mobile = request.data['new_mobile']


                data = {}
                app_user.is_otp_verified = True

                if "whatsapp_update_consent" in request.data:
                    app_user.whatsapp_update_consent = request.data["whatsapp_update_consent"]
                app_user.save()

                #delete all previous token 
                if not request.data.get('is_transaction_pin') == "true":

                    token = LogToken.objects.create(user=user.user)

                transaction_pin = request.data.get('is_transaction_pin',None)
                email = request.data.get('email',None)

                lead_stage = PlatformCentralStagemaster.objects.filter(name__icontains="lead",is_deleted=False).using("fatakpay")

                latest_application = LoanApplication.objects.filter(user=app_user).order_by('-created_at')

                if latest_application.exists():
                    latest_application = latest_application.first()
                    if lead_stage.exists():
                        lead_stage = lead_stage.first()
                        if latest_application.stage_id == lead_stage.id:
                            form_filling_stage = PlatformCentralStagemaster.objects.filter(name__icontains="form filling",is_deleted=False).using("fatakpay")
                            if form_filling_stage.exists():
                                form_filling_stage = form_filling_stage.first()
                                latest_application.stage_id = form_filling_stage.id
                                latest_application.save()



                data["token"] = token.key

                data["user"] = VerifySerializer(app_user, many=False).data

                if "device_details" in request.data:

                    if UserDeviceDetail.objects.filter(
                        user = app_user).exists():
                        fcmObject = UserDeviceDetail.objects.filter(
                            user = app_user)[0]
                    else:
                        fcmObject = UserDeviceDetail(
                        user = app_user)


                    request.data["device_details"]["user"] = app_user.id

                    serializers = AddEditUserDeviceDetailSerializer(data=request.data["device_details"])

                    if serializers.is_valid():
                        serializers.save()

                return Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': messages.OTP_VERIFIED,
                    'data':data},
                    status = status.HTTP_200_OK
                )
        else:
            return Response({
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': messages.OTP_NOT_FOUND_ERROR,
                'data':None},
                status = status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response({
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': handle_errors(serializer.errors),
                'data':None},
                status = status.HTTP_400_BAD_REQUEST)