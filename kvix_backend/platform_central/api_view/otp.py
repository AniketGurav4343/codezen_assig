from rest_framework.views import APIView
from platform_central.api_function_helpers.otp_helper import *
class SendOTP(APIView):
    def get (self,request,format = None):  
        response = send_otp(self, request, format= None)
        return response