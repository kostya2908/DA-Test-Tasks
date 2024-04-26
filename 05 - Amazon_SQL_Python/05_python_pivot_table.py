#Ищем тех, кто купил 6 iPhone и 1 Airpods

import numpy as np
import pandas as pd

orders = pd.read_csv('./orders.csv')
print(f'orders:\n{orders}')

#---------------------------------------------------------------------------------------------
#------------------------------------------ONLY PIVOT_TABLE-----------------------------------
#---------------------------------------------------------------------------------------------
print(orders.sort_values(['Customer_name', 'Prod_Name']).head(15))
pvt_1 = pd.pivot_table(orders.sort_values(['Customer_name', 'Prod_Name']),
                       index='Customer_name',
                       columns='Prod_Name',
                       aggfunc={'Qty': 'sum'})\
                               .fillna(0)\

#выше получилось посчитать результат, используя только сортировку и сводную таблицу.
#для "борьбы" с именами столбцов - или переименовывать вручную или get_level_values,
#т.к. после pivot имена столбцов - комбинация мультииндексов:

print(f'pvt_1:\n{pvt_1}')

pvt_1.columns = pvt_1.columns.get_level_values(level=1)
print(f'pvt_1:\n{pvt_1}')
#print(pvt_1.columns)

#print(pvt_1.index)
#pvt_1.index = pvt_1.index.get_level_values(level=0)
#print(pvt_1)

result_1 = pvt_1[(pvt_1.Airpods == 1) & (pvt_1.iPhone == 6)]
print(f'result_1:\n{result_1}')
#print(f'result_1:\n{result_1.reset_index().Customer_name}')



