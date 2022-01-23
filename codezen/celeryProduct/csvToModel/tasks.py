from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import *
import pandas as pd

@shared_task(bind=True)
def send_mail_func(self):
    print("task asinged !!!!!!!!!!!!!!")
    Product.objects.create(product_name = "aniket",amount = 275.0)
    return "Done"

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


@shared_task
def add():
    print("grate!!!!!!!!!!!!!!!!!!!!!!!")
    print("grate!!!!!!!!!!!!!!!!!!!!!!!")
    print("grate!!!!!!!!!!!!!!!!!!!!!!!")
    return "Done"