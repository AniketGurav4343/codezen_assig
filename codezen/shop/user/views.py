from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework import filters,status
from rest_framework.decorators import api_view,authentication_classes,permission_classes,action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,IsAuthenticatedOrReadOnly,DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly



from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class PlateformAPIMixin:
    def post_request(user,requested_url,requested_data,response_data):
        print(user,requested_url,requested_data,response_data)
        PlatformApiCall.objects.create(user=user,requested_url=requested_url,requested_data=requested_data,response_data=response_data)
        return Response("Data save successfull")


#Product CRUD application
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ProductList_view(request):
    if request.method == 'GET':
        data = Product.objects.all()
        serializer = ProductsSerializer(data, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ProductDetails_view(request, pk):
    if request.method == 'GET':
        data = Product.objects.get(id=pk)
        serializer = ProductsSerializer(data)
        return Response(serializer.data)

#Validation for duplicate product creation
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ProductCreate_view(request):
    serializer = ProductPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ProductUpdate_view(request,pk):
    Pro = Product.objects.get(id=pk)
    serializer = ProductsSerializer(instance=Pro, data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ProductDelete_view(request,pk):
    Pro = Product.objects.get(id=pk)
    Pro.delete()
    return Response("Data delete successfull")
    




#Order CRUD application
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class OrdersList(PlateformAPIMixin, APIView):
    def get(self, request, format=None):
        data = Orders.objects.all()
        serializer = OrdersSerializer(data, many=True)
        user = User.objects.get(id=request.user.id)
        requested_url = 'http://127.0.0.1:8000/OrdersListAPI'
        request_data = 'GET'
        responce_data = serializer.data
        PlateformAPIMixin.post_request(user,requested_url,request_data,responce_data)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrdersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(id=request.user.id)
            requested_url = 'http://127.0.0.1:8000/OrdersListAPI'
            request_data = 'POST',request.data
            responce_data = serializer.data
            PlateformAPIMixin.post_request(user,requested_url,request_data,responce_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersDetail(APIView):
    def get_object(self, pk):
        try:
            return Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = OrdersSerializer(data)
        user = User.objects.get(id=request.user.id)
        requested_url = 'http://127.0.0.1:8000/OrdersListAPI/'+str(pk)+'/'
        request_data = 'GET'
        responce_data = serializer.data
        PlateformAPIMixin.post_request(user,requested_url,request_data,responce_data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = OrdersSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(id=request.user.id)
            requested_url = 'http://127.0.0.1:8000/OrdersListAPI/'+str(pk)+'/'
            request_data = 'PUT',request.data
            responce_data = serializer.data
            PlateformAPIMixin.post_request(user,requested_url,request_data,responce_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Orders = self.get_object(pk)
        Orders.delete()
        user = User.objects.get(id=request.user.id)
        requested_url = 'http://127.0.0.1:8000/OrdersListAPI/'+str(pk)+'/'
        request_data = 'DELETE'
        responce_data = "Order deleted successfully"
        PlateformAPIMixin.post_request(user,requested_url,request_data,responce_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

# Customer
class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    authentication_class = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# Seller
class SellerViewSet(ModelViewSet):
    serializer_class = SellerSerializer
    queryset = Seller.objects.all()
    authentication_class = [TokenAuthentication]
    permission_classes = [IsAuthenticated]




from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#Product filter and search icontain
class OrderProductFilterList(generics.ListAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['products']
    search_fields = ['products__name']

#users filter with ( select related )
class OrdCustSelectList_view(generics.ListAPIView):
    serializer_class = OrdersCustomerSerializer
    queryset = Orders.objects.select_related('Customer').all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Customer']

#Product search filter with( prefetch related )
class OrdProPrefetch_view(generics.ListAPIView):
    serializer_class = OrdProPrefetchSerializer
    queryset = Orders.objects.all().prefetch_related('products')
    filter_backends = [filters.SearchFilter]
    search_fields = ['products__name']


#List API will have sorting ( acending, decending and top 5 )
class OrdersViewSet(ModelViewSet):
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['Customer']

    @action(methods=['get'], detail=False)
    def top5(self, request):
        queryset = self.get_queryset()
        queryset = queryset.order_by('-amount')[:5]
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

#Customer can only view his own List ( use decorator to restrict forbidden users )
@login_required
@api_view(['GET'])
def CustomerOrdersList_view(request):
    if request.method == 'GET':
        data = Orders.objects.filter(Customer=request.user.id)
        serializer = OrdersSerializer(data, many=True)
        return Response(serializer.data)



