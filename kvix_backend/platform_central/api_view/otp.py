from rest_framework.views import APIView
from platform_central.api_function_helpers.otp_helper import *
from platform_central.serializers import *
class SendOTP(APIView):
    serializer_class = SendOtpSerializer
    def post (self,request,format = None):  
        response = send_otp(self, request, format= None)
        return response