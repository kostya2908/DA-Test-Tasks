import numpy as np
import pandas as pd
import json
import hashlib
import matplotlib.pyplot as plt

#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)

#---------------------------------------FIRST STEP-------------------------------------
def get_hash(a, b):
    return hashlib.md5((a + str(b)).encode('utf-8')).hexdigest()

def get_route(lst):
    tmp = [lst[0].get('origin', 'no_data')]
    for i in lst:
        tmp.append(i.get('destination', 'no_data'))
    route = '-'.join(tmp)
    return route 

df = pd.read_csv('./data.csv')
df.iloc[:, -1] = df.iloc[:, -1].apply(lambda x: json.loads(x))
#print(df)
result = df.iloc[:, :]
result['flights_count'] = df['flights_info'].apply(lambda x: len(x))
result['itinerary'] = result['flights_info'].apply(lambda x: get_route(x))
result = result.explode('flights_info').reset_index(drop=True)
result['baggage'] = result['flights_info'].apply(lambda x: x.get('baggage', 'no_data')) 
result['origin'] = result['flights_info'].apply(lambda x: x.get('origin', 'no_data'))
result['destination'] = result['flights_info'].apply(lambda x: x.get('destination', 'no_data'))
result['airline'] = result['flights_info'].apply(lambda x: x.get('airline', 'no_data'))
result['flight_index'] = result.groupby('booking_id')['booking_id'].rank(method='first', ascending=True).astype(int) - 1
result['flight_id'] = result.apply(lambda x: get_hash(x['booking_id'], x['flight_index']), axis=1)
#reordering columns:
cols = ['booking_id', 'booking_month', 'itinerary', 'flights_count', 'flight_id',
        'flight_index', 'origin', 'destination', 'airline', 'baggage', 'passengers', 'price']
result = result[cols]
#print(result.head(50))

#-----------------------------------------SECOND STEP----------------------------------------
#MSK-SPB

ms = result[(result['destination'] == 'LED') &\
        ((result['origin'] == 'SVO') | (result['origin'] == 'VKO') | (result['origin'] == 'DME'))]
#print(ms)
#PIE by airport:

#1. Passengers by SVO, VKO, DME:
pie_psngrs = ms[['origin', 'passengers']].groupby('origin').sum('passengers')\
        .sort_values('passengers', ascending=False)
#print(pssngrs)
one = plt.figure(1, figsize=(4.5, 4.5))
plt.pie(pie_psngrs['passengers'], explode=[0.01, 0.01, 0.01],
        labels=list(pie_psngrs.index), labeldistance=None, autopct='%1.0f%%')  
plt.suptitle('Passengers from MSK to SPB\nby departure airport')
plt.tight_layout()
plt.legend()
plt.savefig('./01_passengers_by_port.png')
plt.close()

#2. Passengers during period:
months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'November', 'December']
time_psngrs = ms[['booking_month', 'passengers']].groupby('booking_month').sum('passengers')
two = plt.figure(2, figsize=(9, 4.5))
ax = two.add_subplot(111)
plt.bar(time_psngrs.index, time_psngrs['passengers'], color='lightblue')
plt.grid(axis='y', ls=':', color='grey')
ax.set(xlabel='Months', ylabel='Quantity of passengers',
       xticklabels=months, title='Passengers Traffic by Months')
ax.bar_label(ax.containers[0])
plt.tight_layout()
plt.savefig('./02_passengers_by_months.png')
plt.close()

#3. Airlines:
ms_gr = ms[['origin', 'airline', 'passengers']].pivot_table(values='passengers',
                                                            index='airline',
                                                            columns='origin',
                                                            aggfunc='sum',
                                                            fill_value=0)
#print(ms_gr)
three = plt.figure(3, figsize=(13.5, 4.5))
svo = three.add_subplot(131)
ms_gr_svo = ms_gr['SVO'][ms_gr['SVO'] > 900].sort_values(ascending=False)
plt.pie(ms_gr_svo, wedgeprops=dict(width=0.67),
        labels=list(ms_gr_svo.index), labeldistance=None, autopct='%1.0f%%')
plt.legend(ncols=3, loc='upper center')
svo.set(title='SVO - Sheremetevo')
plt.tight_layout()

vko = three.add_subplot(132)
ms_gr_vko = ms_gr['VKO'][ms_gr['VKO'] > 800].sort_values(ascending=False)
plt.pie(ms_gr_vko, wedgeprops=dict(width=0.67),
        labels=list(ms_gr_vko.index), labeldistance=None, autopct='%1.0f%%')
plt.legend(ncols=3, loc='upper center')
vko.set(title='VKO - Vnukovo')
plt.tight_layout()

dme = three.add_subplot(133)
ms_gr_dme = ms_gr['DME'][ms_gr['DME'] > 200].sort_values(ascending=False)
plt.pie(ms_gr_dme, wedgeprops=dict(width=0.67),
        labels=list(ms_gr_dme.index), labeldistance=None, autopct='%1.0f%%')
plt.legend(ncols=3, loc='upper center')
dme.set(title='DME - Domodedovo')
plt.tight_layout()
plt.savefig('./03_airlines.png')

#The airline with cheapest ticket MSK-SPB:
ms['price_per_person'] = round(ms['price'] / ms['passengers'], 1)
#print(ms.loc[ms.groupby('airline')['price_per_person'].idxmin()].sort_values('price'))

#The largest revenue (sum and avg):
revenue = ms.groupby('airline').agg(total=('price', 'sum'), per_person=('price_per_person', 'mean')).round(2)
revenue_total = revenue['total'].sort_values(ascending=False)
revenue_avg = revenue['per_person'].sort_values(ascending=False)

print(revenue)
print(revenue_total.head(3))
print(revenue_avg.head(3))

