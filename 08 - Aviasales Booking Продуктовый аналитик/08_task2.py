import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.lines import Line2D

#pd.set_option('display.max_columns', None)

df = pd.read_csv('./booking_analytics_test_df.csv')
print(df)
print(df[df['service'].isna()])

#1. При помощи Pandas соберите таблицу, где в строках будет наименование услуги,
#а в столбцах минимальная и максимальная цена услуги,
#минимальный и максимальный профит от услуги, количество заказов с услугой
cols = ['service', 'service_price', 'service_profit', 'order_id']
'''
#Все заказы:
part_1 = df[cols]\
        .pivot_table(values=['service_price', 'service_profit', 'order_id'],
                     index='service',
                     aggfunc={'service_price': ['max', 'min'],
                              'service_profit': ['max', 'min'],
                              'order_id': ['count',]},
                     dropna=True, margins=False, sort=False)\
                             .round(2)
'''
#Заказы с доп. услугами:
part_1 = df[~df['service'].isna()][cols]\
        .pivot_table(values=['service_price', 'service_profit', 'order_id'],
                     index='service',
                     aggfunc={'service_price': ['max', 'min'],
                              'service_profit': ['max', 'min'],
                              'order_id': ['count',]},
                     dropna=True, margins=False, sort=False)\
                             .round(2)
part_1 = part_1.reindex(columns=[('service_price','min'),
                                 ('service_price','max'),
                                 ('service_profit','min'),
                                 ('service_profit','max'),
                                 ('order_id', 'count')])
print(part_1)

#2. При помощи Pandas соберите таблицу, где в строках будет наименование услуги,
#а в столбцах цена и профит услуг по топ-5 странам вылета по продажам билетов.
top_5 = df.groupby('origin_country')['order_id']\
        .count().sort_values(ascending=False)\
        .head(5)\
        .index\
        .to_list()
#print(top_5)
part_2 = df[df['origin_country'].isin(top_5)]\
        .pivot_table(values=['service_price', 'service_profit'],
                     index='service',
                     columns='origin_country',
                     aggfunc={'service_price': ['mean',],
                              'service_profit': ['mean',]})\
                                      .round(2)\
                                      .fillna(0)
#print(part_2)

#3. При помощи любой библиотеки визуализируйте динамику профита, оборота,
#доли профита от оборота по заказам с услугами. Опишите распределения и сделайте выводы.

def get_color(pctg, dow):
    if pctg > 100:
        return 'silver'
    else:
        if dow:
            return 'red'
        else:
            return 'orange'

df['service_price'].fillna(0, inplace=True)
#print(df[~df['service'].isna()])

df['order_date'] = pd.to_datetime(df['order_date'])
part_3 = df[~df['service'].isna()]\
        .groupby('order_date')[['service_price', 'service_profit']]\
        .sum()\
        .round(2)
part_3['profit_portion'] = (100 * part_3['service_profit'] / part_3['service_price'])\
        .round(2)
part_3.reset_index(inplace=True)

part_3['weekend'] = part_3['order_date'].dt.dayofweek > 4 
part_3['color'] = part_3\
        .apply(lambda x: get_color(x['profit_portion'], x['weekend']), axis=1)
part_3.drop('weekend', axis=1, inplace=True)
part_3['price_roll'] = part_3['service_price']\
        .rolling(7, min_periods=1, center=True)\
        .mean().round(2)
part_3['profit_roll'] = part_3['service_profit']\
        .rolling(7, min_periods=1, center=True)\
        .mean().round(2)
print(part_3)        
fig, ax = plt.subplots(3, 1, figsize=(18, 9))
units = ['RUB', 'RUB', '%']
for i, v in enumerate(list(part_3.columns)[1:4]):
    ax[i].bar(part_3['order_date'], part_3[v], color=part_3['color'])
    ax[i].set_xticks(part_3['order_date'])
    ax[i].tick_params(axis='x', labelsize=7, labelrotation=90)
    ax[i].grid(axis='y', ls=':', color='grey')
    ax[i].set(title=f"{(' '.join(v.split('_'))).title()}, {units[i]}")
#Rolling averages:
ax[0].plot(part_3['order_date'], part_3['price_roll'], color='blue', ls='dashed',
           label='Rolling Average (7 days)', alpha=0.35)
ax[1].plot(part_3['order_date'], part_3['profit_roll'], color='blue', ls='dashed',
           label='Rolling Average (7 days)', alpha=0.35)
#Legend (manually):
colors = {'Weekdays': 'orange', 'Weekends': 'red',
          'Incorrect Data': 'silver', 'Rolling AVG': 'blue'}
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels[:-1]]
line = Line2D([0], [0], label=labels[3], color=colors['Rolling AVG'], ls='dashed', alpha=0.35)
handles.extend([line])
ax[0].legend(handles, labels)
ax[1].legend(handles, labels)
ax[2].legend(handles[:-1], labels, loc='upper left')
plt.tight_layout()
plt.savefig('./service_dynamics.png')
plt.show()

