from os import set_inheritable
from rest_framework.response import Response
from rest_framework import status
from common import messages

def upload_profile(self,request):
    
    serializer = self.serializer_class(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': messages.DOCUMENT_UPLOADED,
                    'data':serializer.data},
                    status = status.HTTP_200_OK)
    else:
        return Response({
                        'success': False,
                        'status_code': status.HTTP_200_OK,
                        'message': "handle_errors(serializer.errors)",
                        'data':None},
                        status = status.HTTP_200_OK)

def create_customer(self,request):
    
    serializer = self.serializer_class(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': messages.DOCUMENT_UPLOADED,
                    'data':serializer.data},
                    status = status.HTTP_200_OK)
    else:
        return Response({
                        'success': False,
                        'status_code': status.HTTP_200_OK,
                        'message': "handle_errors(serializer.errors)",
                        'data':None},
                        status = status.HTTP_200_OK)

