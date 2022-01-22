from django.core.management.base import BaseCommand
from csvToModel.models import Product
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):
        # data = pd.read_excel('./static/excel/Product_data.xlsx', index_col=0)
        # df = pd.DataFrame(data)
        # for i,row in df.iterrows():
        #     duplicate = Product.objects.filter(product_name = i)
        #     if duplicate:
        #         pass
        #     else:
        #         Product.objects.create(product_name = i,amount = row[0],)
        self.stdout.write('Product Added Successfully!!!!!!!!')