from django.shortcuts import render,HttpResponse
from .models import Product
from .tasks import *
from .management.commands import member
# Create your views here.
import pandas as pd
def Product_view(request):
    get_exchange_rate.delay()
    # data = pd.read_excel('./static/excel/Product_data.xlsx', index_col=0) 
    # df = pd.DataFrame(data)
    # for i,row in df.iterrows():
    #     duplicate = Product.objects.filter(product_name = i)
    #     if duplicate:
    #         pass
    #     else:
    #         Product.objects.create(product_name = i,amount = row[0],)
    return HttpResponse("success") 

def celery_task_view(request):
    add.delay(5,3)
    return HttpResponse("<h1>hello server</h1>") 
