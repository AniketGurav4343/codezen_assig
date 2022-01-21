from django.shortcuts import render,HttpResponse
from .models import Product
# Create your views here.
import pandas as pd
def Product_view(request):
    data = pd.read_excel('./static/excel/Product_data.xlsx', index_col=0) 
    df = pd.DataFrame(data)
    for i,row in df.iterrows():
        duplicate = Product.objects.filter(product_name = i)
        if duplicate:
            pass
        else:
            Product.objects.create(product_name = i,amount = row[0],)
    return HttpResponse("success") 