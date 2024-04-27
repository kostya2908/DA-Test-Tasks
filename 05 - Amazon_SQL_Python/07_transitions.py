import numpy as np
import pandas as pd

df = pd.read_csv('./transitions.csv')
print(df)

def get_event(a, b):
    tup = (a, b)
    match tup:
        case ('Free', 'Paid'):
            return 'Convert'
        case ('Paid', 'Free'):
            return 'ReverseConvert'
        case ('Paid', 'Non-member'):
            return 'Cancel'
        case ('Free', 'Non-member'):
            return 'Cancel'
        case ('Non-member', 'Paid'):
            return 'ColdStart'
        case ('Non-member', 'Free'):
            return 'WarmStart'
        case ('Paid', 'Paid'):
            return 'Renewal'
        case ('Free', 'Free'):
            return 'Renewal'

df.sort_values(['customer_id',
               'membership_start_date',
               'membership_end_date'],
               inplace=True)
#print(df.iloc[:, -3:])
df['shift'] = df['membership_status'].shift(-1)
#print(df.iloc[:, -3:])
df['event'] = df.apply(lambda x: get_event(x['membership_status'], x['shift']), axis=1)
#print(df.iloc[:, -3:])
result = df.iloc[:-1, [0, 2, 5]]
result.rename(columns={'membership_end_date': 'change_date'}, inplace=True)
print(f'result:\n{result}')
