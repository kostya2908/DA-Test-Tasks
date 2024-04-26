import numpy as np
import pandas as pd

size = 3000
n_customers = 200
customer_id = np.random.randint(1, n_customers + 1, size=size).tolist()
products = ['iPhone', 'iPad', 'Airpods', 'shirt', 'shoes', 'pants', 'MacBook', 'AppleWatch']
prod_name = []
for i in range(size):
    prod_name.append(products[np.random.randint(0, len(products))])
print(set(customer_id))
print(set(prod_name))

orders = pd.DataFrame(
        {'customer_id': customer_id,
         'prod_name': prod_name
         })

print(f'orders:\n{orders}')

orders = orders.sort_values(['customer_id', 'prod_name'])

o_grouped = orders\
        .groupby(['customer_id', 'prod_name'])\
        .agg(quantity=('prod_name', 'count'))\

o_grouped.reset_index(drop=True)



print(f'o_grouped:\n{o_grouped}')

pvt = pd.pivot_table(o_grouped,
                     values='quantity',
                     index='customer_id',
                     columns='prod_name',
                     aggfunc='first')\
                             .fillna(0)\
                             #.reset_index()#drop=True)
print(f'pvt:\n{pvt}')

result = pvt[(pvt.Airpods == 0) & (pvt.iPhone > 3)]

print(f'result:\n{result}')
result.reset_index(inplace=True)
print(f'result:\n{result}')







