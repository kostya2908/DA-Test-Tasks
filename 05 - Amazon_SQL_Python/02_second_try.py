import numpy as np
import pandas as pd

size = 3000
n_customers = 200
customer_id = np.random.randint(1, n_customers + 1, size=size).tolist()
products = ['iPhone', 'iPad', 'Airpods', 'shirt', 'shoes', 'pants', 'MacBook', 'AppleWatch']
prod_name = []
for i in range(size):
    prod_name.append(products[np.random.randint(0, len(products))])
#print(set(customer_id))
#print(set(prod_name))

orders = pd.DataFrame(
        {'customer_id': customer_id,
         'prod_name': prod_name
         })

#print(f'orders:\n{orders}')

#---------------------------------------------------------------------------------------------
#------------------------------------------ONLY PIVOT_TABLE-----------------------------------
#---------------------------------------------------------------------------------------------
print(orders.sort_values(['customer_id', 'prod_name']).head(15))
pvt_1 = pd.pivot_table(orders.sort_values(['customer_id', 'prod_name']),
                       index='customer_id',
                       columns='prod_name',
                       aggfunc={'prod_name': 'count'})\
                               .fillna(0)\
                               #.reset_index()#drop=True)

#выше получилось посчитать результат, используя только сортировку и сводную таблицу.
#для "борьбы" с именами столбцов - или переименовывать вручную или get_level_values,
#т.к. после pivot имена столбцов - комбинация мультииндексов.

print(f'pvt_1:\n{pvt_1}')#.to_string()}')
'''
print(pvt_1.columns)
pvt_1.reset_index(inplace=True)
print(pvt_1)
print(pvt_1.columns)
pvt_1.columns = ['customer_id', 'Airpods', 'AppleWatch',\
        'MacBook', 'iPad', 'iPhone', 'pants', 'shirt', 'shoes']
print(pvt_1)
'''
pvt_1.columns = pvt_1.columns.get_level_values(level=1)
print(f'pvt_1:\n{pvt_1}')
#print(pvt_1.columns)

#pvt_1 = pvt_1.rename_axis(None, axis=1)
print(pvt_1.index)
pvt_1.index = pvt_1.index.get_level_values(level=0)

print(pvt_1)

result_1 = pvt_1[(pvt_1.Airpods == 0) & (pvt_1.iPhone > 3)]
print(f'result_1:\n{result_1}')
print(f'result_1:\n{result_1.reset_index().customer_id}')



#---------------------------------------------------------------------------------------------
#-------------------------------------GROUPBY + PIVOT_TABLE-----------------------------------
#---------------------------------------------------------------------------------------------
o_grouped = orders\
        .groupby(['customer_id', 'prod_name'])\
        .agg(quantity=('prod_name', 'count'))\

o_grouped.reset_index(drop=True)
print(f'o_grouped:\n{o_grouped.head(15)}')

pvt_2 = pd.pivot_table(o_grouped,
                       values='quantity',
                       index='customer_id',
                       columns='prod_name',
                       aggfunc='first')\
                               .fillna(0)\
                               #.reset_index()#drop=True)
print(f'pvt_2:\n{pvt_2}')
result_2 = pvt_2[(pvt_2.Airpods == 0) & (pvt_2.iPhone > 3)]
print(f'result_2:\n{result_2}')
result_2.reset_index(inplace=True)
print(f'result_2:\n{result_2.customer_id}')


#--------------------------------------------------------------------------------------------
#-----------------------------------ONLY PIVOT-----------------------------------------------
#--------------------------------------------------------------------------------------------

extra_data = np.random.randint(1000, 1050, size=size)
#extra_data = [i for i in range(543,3543)]
print(set(extra_data))
orders['extra_data'] = extra_data
print(f'orders:\n{orders}')
orders.sort_values(['customer_id', 'prod_name'], inplace=True)
print(f'orders:\n{orders}')


pvt_3 = orders.pivot(index='extra_data',
                     columns='prod_name',
                     values='customer_id')
print(pvt_3)
#этим способом можно получить UNSTACKED таблицу, только если индексы уникальны.
#в моем случае это невозможно
#---------------------------------------------------------------------------------------------









