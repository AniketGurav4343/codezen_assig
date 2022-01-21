from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from user.views import SellerViewSet,CustomerViewSet,OrdersViewSet,CustomAuthToken
router=DefaultRouter()

router.register('SellerAPI',views.SellerViewSet,basename='SellerAPI')
router.register('CustomersAPI',views.CustomerViewSet,basename='CustomersAPI')

#List API will have sorting ( acending, decending and top 5 )
router.register('OrdersAPI',views.OrdersViewSet,basename='OrdersAPI')



urlpatterns = [
    path('api/',include(router.urls)),
    
    #Product CRUD application
    path('Product-list', views.ProductList_view, name='Product-list'),
    path('Product-details/<int:pk>/', views.ProductDetails_view, name='Product-details'),
    #Validation for duplicate product creation
    path('Product-create', views.ProductCreate_view, name='Product-create'),
    path('Product-update/<int:pk>/', views.ProductUpdate_view, name='Product-update'),
    path('Product-delete/<int:pk>/', views.ProductDelete_view, name='Product-delete'),

    #Order CRUD application
    path('OrdersListAPI', views.OrdersList.as_view()),
    path('OrdersListAPI/<int:pk>/', views.OrdersDetail.as_view()),
    
    #Product filter and search icontain
    path('OrderProductFilterAPI', views.OrderProductFilterList.as_view()),
    
    #users filter with ( select related )
    path('OrdCustSelectListAPI',views.OrdCustSelectList_view.as_view()),
    
    #Product search filter with( prefetch related )
    path('OrdProPrefetchAPI',views.OrdProPrefetch_view.as_view()),

    #Customer can only view his own List ( use decorator to restrict forbidden users )
    path('CustomerOrder-list', views.CustomerOrdersList_view, name='CustomerOrder-list'),

    
    
    
    path('gettoken/', CustomAuthToken.as_view()),

    path('a', views.a, name='a'),
    path('Product_pd_view', views.Product_view, name='Product_pd_view'),
]














    # path('Order-list', views.OrdersList_view, name='Order-list'),
    # path('Order-details/<int:pk>/', views.OrdersDetails_view, name='Order-details'),
    # path('Order-create', views.OrdersCreate_view, name='Order-create'),
    # path('Order-update/<int:pk>/', views.OrdersUpdate_view, name='Order-update'),
    # path('Order-delete/<int:pk>/', views.OrdersDelete_view, name='Order-delete'),