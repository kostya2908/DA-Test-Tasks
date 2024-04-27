import numpy as np
import pandas as pd

cust_id = []
for i in range(1000):
    cust_id.append(np.random.randint(1, 101)) #100 unique customers
start = pd.date_range(start='1982-10-16', end='2007-02-15', freq='2D').to_list()[:len(cust_id)]
end = pd.date_range(start='1983-02-28', end='2017-08-01', freq='5D').to_list()[:len(cust_id)]
status_set = ['Free', 'Paid', 'Non-member']
status = []
for i in range(len(cust_id)):
    status.append(status_set[np.random.randint(0, len(status_set))])
df = pd.DataFrame(
        {'customer_id': cust_id,
         'membership_start_date': start,
         'membership_end_date': end,
         'membership_status': status})
#print(df)
#фильтрация изменений статуса:
df.sort_values(['customer_id',
                'membership_start_date',
                'membership_end_date'],
               inplace=True)
#print(df)
df['shift'] = df.membership_status.shift(-1)
df['flag'] = df.apply(lambda x: 
                      False if (x['membership_status'] == x['shift'])\
                              and (x['shift'] != 'Paid')\
                              and (x['shift'] != 'Free')
                      else True,
                      axis=1)
df = df[df.flag == True].drop(['shift', 'flag'], axis=1).reset_index(drop=True)
print(df)
df.to_csv('./transitions.csv', index=False)

