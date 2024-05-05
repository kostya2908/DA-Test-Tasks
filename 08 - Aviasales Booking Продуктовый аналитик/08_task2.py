import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.lines import Line2D

pd.set_option('display.max_columns', None)

df = pd.read_csv('./booking_analytics_test_df.csv')
print(df)
#print(df[df['service'].isna()])

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
#print(part_1)

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
#print(part_3)        
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
plt.close()

#4. Сравните распределения цен заказов в зависимости от платформы, сделайте выводы.
platforms = df['order_platform'].dropna().unique()
platforms = np.sort(platforms)
#print(platforms)
platforms = np.concatenate([platforms[:2], np.roll(platforms[2:-1], -1), platforms[-1:]])
#print(platforms)
fig, ax = plt.subplots(3, 2, figsize=(18, 9))
for i, v in enumerate(platforms):
    ax[i//2, i%2].hist(df[df['order_platform'] == v]['order_price'], bins=100, log=False,
                       rwidth=0.95)
    ax[i//2, i%2].set(title=(' '.join(v.split('_'))).title(),
                      xlim=(0, df[df['order_platform'] == v]['order_price'].mean() +\
                              df[df['order_platform'] == v]['order_price'].std() * 2))
    ax[i//2, i%2].ticklabel_format(style='plain', useOffset=True)
plt.tight_layout()
plt.savefig('./order_price_distribution.png')
plt.close()

#5. Проанализируйте зависимость глубины бронирования от цены и сделайте выводы.
part_5 = df[df['booking_depth'] > 7][['order_price', 'booking_depth']].sort_values('order_price')
part_5['depth_roll'] = part_5['booking_depth'].rolling(250, min_periods=1, center=True).mean()
fig, ax = plt.subplots(2, 1, figsize=(18, 9))
ax[0].plot(part_5['order_price'], part_5['booking_depth'].round(0), color='silver',
        label='Booking Depth')
ax[0].plot(part_5['order_price'], part_5['depth_roll'], color='blue', linewidth=0.75,
        label='Rolling Average (250 values)')
ax[0].set(title='Booking Depth by Order Price (Price less than 100k RUB)',
       xlabel='Order Price, RUB', ylabel='Booking Depth, days',
       xlim=(0, 100000))
ax[0].ticklabel_format(style='plain', useOffset=True)
ax[0].grid(axis='y', ls=':', color='black')
ax[0].legend()

ax[1].plot(part_5['order_price'], part_5['booking_depth'].round(0), color='silver',
        label='Booking Depth')
ax[1].plot(part_5['order_price'], part_5['depth_roll'], color='blue', linewidth=0.75,
        label='Rolling Average (250 values)')
ax[1].set(title='Booking Depth by Order Price (Price more than 100k RUB)',
       xlabel='Order Price, RUB', ylabel='Booking Depth, days',
       xlim=(100000, part_5['order_price'].max()))
ax[1].ticklabel_format(style='plain', useOffset=True)
ax[1].grid(axis='y', ls=':', color='black')
ax[1].legend()

plt.tight_layout()
plt.savefig('./booking_depth.png')
plt.close()

