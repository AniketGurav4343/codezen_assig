from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import *
import pandas as pd


@shared_task(bind=True)
def csvToModeldata(self):
    data = pd.read_excel('./static/excel/Product_data.xlsx', index_col=0) 
    df = pd.DataFrame(data)
    for i,row in df.iterrows():
        duplicate = Product.objects.filter(product_name = i)
        if duplicate:
            pass
        else:
            Product.objects.create(product_name = i,amount = row[0],)
    print("grate!!!!!!!!!!!!!!!!!!!!!!!")
    return "Done"
