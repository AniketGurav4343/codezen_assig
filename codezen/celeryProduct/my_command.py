import pandas as pd

excel_file = './excel/Product_data.xlsx'

df = pd.read_excel(excel_file)

print(df)