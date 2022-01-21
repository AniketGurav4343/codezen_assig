
@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def OrdersList_view(request):
    if request.method == 'GET':
        data = Orders.objects.all()
        serializer = OrdersSerializer(data, many=True)
        filter_backends = [filters.SearchFilter]
        search_fields = ['products']
        return Response(serializer.data)
        

@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def OrdersDetails_view(request, pk):
    if request.method == 'GET':
        data = Orders.objects.get(id=pk)
        serializer = OrdersSerializer(data)
        return Response(serializer.data)

@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def OrdersCreate_view(request):
    serializer = OrdersSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
@api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def OrdersUpdate_view(request,pk):
    Ord = Orders.objects.get(id=pk)
    serializer = OrdersSerializer(instance=Ord, data=request.data)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

    
@api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def OrdersDelete_view(request,pk):
    Ord = Orders.objects.get(id=pk)
    Ord.delete()
    return Response("Data delete successfull")