import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('./06_apalon_app_usage.csv')
print(df.iloc[:, :4])
df['Date'] = pd.to_datetime(df['Date'], format='mixed')
df.set_index('Date', inplace=True)
df['Median Session Length'] = pd.to_timedelta(df['Median Session Length'])

df['Total Time Spent in App by all users'] = \
        df['Total Time Spent in App by all users'].str.replace('yr', 'years')
df['Total Time Spent in App by all users'] = \
        df['Total Time Spent in App by all users'].str.replace('mo', 'months')
df['Total Time Spent in App by all users'] = \
        df['Total Time Spent in App by all users'].str.replace('dy', 'days')
df['Total Time Spent in App by all users'] = \
        df['Total Time Spent in App by all users'].str.replace('hr', 'hours')
df['Avg Session Length'] = pd.to_timedelta(df['Avg Session Length'])

def get_days(x):
    tmp = x.split()
    z = {'years': 0, 'months': 0, 'days': 0, 'hours': 0, 'min': 0, 'sec': 0}
    z.update(dict(zip(tmp[1::2], tmp[::2])))
    result = int(z['years'])*365 + int(z['months'])*30 + int(z['days'])
    z.update({'days': result})
    del z['years'], z['months']
    string = ''
    for i in z:
        string += str(z[i]) + ' ' + i + ' '
        string.rstrip()
    return string

df['Total Time Spent in App by all users'] = df['Total Time Spent in App by all users'].apply(lambda x: get_days(x))
df['Total Time Spent in App by all users'] = \
        pd.to_timedelta(df['Total Time Spent in App by all users'])\
        .round('d')


print(df.iloc[:,[0,1,2,3]])

#----------------------------------------------------------------------------------

#Total Time Spent:
plt.figure(1, figsize=(19, 4.5))
plt.plot(df.iloc[:, 1], label=df.columns[1])
plt.legend()
plt.grid(axis='both', ls=':', color='grey')
plt.tick_params(axis='x', labelrotation=90, labelsize=8)
plt.subplot(111).set(title=df.columns[1])
plt.xticks(df.index[::3])
plt.tight_layout()

#Sessions:
plt.figure(2, figsize=(19, 4.5))
plt.plot(df.iloc[:, 5], label=df.columns[5])
plt.legend()
plt.grid(axis='both', ls=':', color='grey')
plt.tick_params(axis='x', labelrotation=90, labelsize=8)
plt.subplot(111).set(title=df.columns[5])
plt.xticks(df.index[::3])
plt.tight_layout()

#Active Users:
plt.figure(3, figsize=(19, 4.5))
plt.plot(df.iloc[:, 4], label=df.columns[4])
plt.legend()
plt.grid(axis='both', ls=':', color='grey')
plt.tick_params(axis='x', labelrotation=90, labelsize=8)
plt.subplot(111).set(title=df.columns[4])
plt.xticks(df.index[::3])
plt.tight_layout()

#New Users:
plt.figure(4, figsize=(19, 4.5))
plt.plot(df.iloc[:, 3], label=df.columns[3])
plt.legend()
plt.grid(axis='both', ls=':', color='grey')
plt.tick_params(axis='x', labelrotation=90, labelsize=8)
plt.subplot(111).set(title=df.columns[3])
plt.xticks(df.index[::3])
plt.tight_layout()

#Users Counts:
users_fields = df.iloc[:, 6:13].columns.to_list()
plt.figure(5, figsize=(19, 9))
for i, field in enumerate(users_fields):
    plt.plot(df[field], label=field)
plt.subplot(111).set(title='Users per No. of Sessions')
plt.legend()
plt.grid(axis='both', ls=':', color='grey')
plt.tick_params(axis='x', labelrotation=90, labelsize=8)
plt.xticks(df.index[::3])
plt.tight_layout()


plt.show()

