# from asyncio.proactor_events import constants
# from encodings import utf_8
# from django.conf import settings
# from django.db.models import Q
# import datetime
# import hashlib
# import logging
# import json
# import pytz
# import random

  
# from django.core.mail import EmailMessage

# from itertools import chain

# from datetime import date

# from django.http import HttpResponse
# from django.core import serializers

# from common import messages
# from fatakpay_backend.utils import custom_exceptions as ce

# from miscellaneous.serializers import *

# from rest_framework.response import Response
# from rest_framework import status
# from fatakpay_backend.settings import *
# import boto3
# from django.template.loader import get_template
# from botocore.exceptions import ClientError

# # Get an instance of logger
# logger = logging.getLogger('miscellaneous')

# def send_emailer(self, request, format= None):
#     try:

#         if "template" in request.data:
#             # template = get_template(request.data["template"])
#             template = get_template('email_otp.html', )

#             email_msg = template.render(request.data)

#         else:
#             template = None

#             email_msg = request.data["body_text"]
    
#         # Create a new SES resource and specify a region.
#         client = boto3.client('ses',region_name=AWS_REGION,
#             aws_access_key_id=AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
#         try:
#             if template:
#                 response = client.send_email(
#                     Destination={
#                         'ToAddresses': [
#                             request.data["recipient"],
#                         ],
#                     },
#                     Message={
#                         'Body': {
#                             'Html': {
#                                 'Charset': CHARSET,
#                                 'Data': email_msg,
#                             },
#                         },
#                         'Subject': {
#                             'Charset': CHARSET,
#                             'Data': request.data["subject"],
#                         },
#                     },
#                     Source=EMAIL_SENDER,
#                 )
#             else:
#                 response = client.send_email(
#                     Destination={
#                         'ToAddresses': [
#                             request.data["recipient"],
#                         ],
#                     },
#                     Message={
#                         'Body': {
#                             'Text': {
#                                 'Charset': CHARSET,
#                                 'Data': email_msg,
#                             },
#                         },
#                         'Subject': {
#                             'Charset': CHARSET,
#                             'Data': request.data["subject"],
#                         },
#                     },
#                     Source=EMAIL_SENDER,
#                 )

#                 print(response)
#                 print(request.data["recipient"])


#             return Response({
#                     'success': True,
#                     'status_code': status.HTTP_200_OK,
#                     'message': messages.EMAIL_SENT,
#                     'data':None},
#                     status = status.HTTP_200_OK)


#         # Display an error if something goes wrong.	
#         except ClientError as a:

#             return Response({
#                     'success': False,
#                     'status_code': status.HTTP_200_OK,
#                     'message': messages.EMAIL_INVALID,
#                     'data':a.response['Error']['Message']},
#                     status = status.HTTP_200_OK)

#     except NameError as e:
#         logger.error('SEND EMAIL HELPER HELPER: {}'.format( e))
#         raise ce.NameErrorCe

#     except AttributeError as e:
#         logger.error('SEND EMAIL HELPER HELPER: {}'.format( e))
#         raise ce.AttributeErrorCe

#     except KeyError as e:
#         logger.error('SEND EMAIL HELPER HELPER: {}'.format( e))
#         raise ce.KeyErrorCe

#     except UnboundLocalError as e:
#         logger.error('SEND EMAIL HELPER HELPER: {}'.format( e))
#         raise ce.UnknownColumnError

#     except Exception as e:
#         logger.error('SEND EMAIL HELPER HELPER: {}'.format( e))
#         raise ce.InternalServerError




# def otp_verification(first_name, code, to):

#     client = boto3.client('ses',region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

#     template = get_template('email_otp.html')
#     email_msg = template.render({
#         'first_name': first_name,
#         'code': code
#     })

#     try:
#         response = client.send_email(
#             Destination={
#                 'ToAddresses': [to]
#             },
#             Message={
#                 'Body': {
#                     'Html': {
#                         'Charset': CHARSET,
#                         'Data': email_msg,
#                     },
#                 },
#                 'Subject': {
#                     'Charset': CHARSET,
#                     'Data': "No-Reply: Email Verification for Fatakpay",
#                 },
#             },
#             Source=EMAIL_SENDER,
#         )

#     except Exception as e:
#         print("except")
#         print(e)
#         pass




# def email_for_new_account_password(to, password, username,user_type):
#     client = boto3.client('ses',region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

#     template = get_template('admin_company_registeration.html')
#     email_msg = template.render({
#         'password': password,
#         "username":username,
#         "user_type":user_type
#     })

#     try:
#         response = client.send_email(
#             Destination={
#                 'ToAddresses': [to]
#             },
#             Message={
#                 'Body': {
#                     'Html': {
#                         'Charset': CHARSET,
#                         'Data': email_msg,
#                     },
#                 },
#                 'Subject': {
#                     'Charset': CHARSET,
#                     'Data': "No-Reply: Welcome To Fatakpay",
#                 },
#             },
#             Source=EMAIL_SENDER,
#         )

#     except Exception as e:
#         print("except")
#         print(e)
#         pass