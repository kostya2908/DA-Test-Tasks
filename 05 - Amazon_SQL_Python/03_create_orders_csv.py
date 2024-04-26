import numpy as np
import pandas as pd

size = 500
unique_names = ['Anna', 'Nastya', 'Viktor', 'Vladimir', 'Alexander',\
        'Ivan', 'Sergey', 'Iliya', 'Petr', 'Arni',\
        'Silvy', 'Cortny', 'Steven', 'Bob', 'James',\
        'Elvis', 'Kurt', 'Richie', 'Bluey', 'Bingo',\
        'Shaya', 'Tirion', 'Serceya', 'Ned', 'John',\
        'Mariko', 'Joclyn Stone', 'Monica', 'Cory Chase', 'JollaPr']
names = []
for i in range(size):
    names.append(unique_names[np.random.randint(0, len(unique_names))])
#print(names)

dates = pd.date_range(start='1953-09-03', end='2017-08-01', freq='13D').to_list()[:len(names)]
#print(dates)

order_id = [_ for _ in range(1, len(names)+1)]
#print(order_id)

products = ['iPhone', 'iPad', 'Airpods', 'shirt', 'shoes', 'pants', 'MacBook', 'AppleWatch']
prod_name = []
for i in range(len(names)):
    prod_name.append(products[np.random.randint(0, len(products))])
#print(prod_name)

qty = []
for i in range(len(names)):
    qty.append(np.random.randint(1, 5))
#print(qty)

price = []
for i in range(len(names)):
    price.append(np.random.randint(500, 1990) + 0.99)
#print(price)

df = pd.DataFrame(
        {'Customer_name': names,
         'Order_day': dates,
         'Order_Id': order_id,
         'Prod_Name': prod_name,
         'Qty': qty,
         'Price': price})
print(df)

df.to_csv('/home/kostya/DA Test Tasks/05 - Amazon_SQL_Python/orders.csv', index=False)

