from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from customer.serializers import *
from customer.api_function_helper.customer_helper import *

class CustomerUploadPicture(APIView):
    
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    serializer_class = CustomerProfilePictureSerializer

    # @transaction.atomic
    def post(self,request,format=None):
            response = upload_profile(self,request)
            return response


class CustomerRegister(APIView):
    
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    serializer_class = CustomerUserSerializer

    # @transaction.atomic
    def post(self,request,format=None):
            response = create_customer(self,request)
            return response
