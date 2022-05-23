from urllib.parse import urlencode
import requests
import logging
import os
import boto3
from botocore.exceptions import ClientError

from platform_central.models import SmsCentral

from common.constants import GUPSHUP_TXN_USER_ID, GUPSHUP_TXN_USER_PASSWORD, GUPSHUP_USER_ID, GUPSHUP_USER_PASSWORD

import urllib

CHARSET = "UTF-8"

class dummyresponse(object):
    status_code = 1

    def __init__(self):
        return



def sendGupShupSMS(message, phone, smstype=None):

    query_params = {
        "method":"sendMessage", 
        "send_to":phone, 
        "msg": message, 
        "msg_type":"TEXT", 
        "userid":GUPSHUP_TXN_USER_ID, 
        "auth_scheme":"PLAIN", 
        "password":GUPSHUP_TXN_USER_PASSWORD, 
        "format":"JSON", 
        "v":"1.1", 
        "mask":"124343"}



    r = requests.get("https://enterprise.smsgupshup.com/GatewayAPI/rest", 
        params=query_params, 
        headers={'Accept': '*'})


    print(r.text)

    returnresponse = dummyresponse()
    returnresponse.status_code = r.status_code

    sms_central = SmsCentral(mobile = phone, message = message, url = query_params, response = r.status_code)
    sms_central.save()

    return returnresponse
 
