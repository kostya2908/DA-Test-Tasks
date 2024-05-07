import pandas as pd
from datetime import date

#pd.set_option('display.max_columns', None)
df = pd.read_csv('./task_1_events.csv')

#-------------------------------------TASK No.1-----------------------------------
df['ts'] = pd.to_datetime(df['ts'])
df['pdate'] = pd.to_datetime(df['pdate']).dt.date
df['ts_shift-'] = df['ts'].shift(1)
df['ts_shift+'] = df['ts'].shift(-1)
df['user_id_shift-'] = df['user_id'].shift(1)
df['user_id_shift+'] = df['user_id'].shift(-1)
df['date_shift-'] = df['pdate'].shift(1)
df['date_shift+'] = df['pdate'].shift(-1)

def get_new_session_from_delta(a, B, c, d=None):
    if a != a or a == None or c != c or c == None:
        return True
    elif B - a > d or c - B > d:
        return True
    else:
        return False

def get_new_session_from_cat(a, B, c):
    if a == None or c == None:
        return True
    elif a != B or c != B:
        return True
    else:
        return False

#Check 'ts':
df['check_ts'] = df.apply(lambda x: get_new_session_from_delta(x['ts_shift-'],
                                                               x['ts'],
                                                               x['ts_shift+'],
                                                               pd.to_timedelta('30m')),
                          axis=1)
df = df.drop(df[['ts_shift-', 'ts_shift+']], axis=1)
#Check 'pdate':
df['check_pdate'] = df.apply(lambda x: get_new_session_from_delta(x['date_shift-'],
                                                                  x['pdate'],
                                                                  x['date_shift+'],
                                                                  pd.to_timedelta('23:59:59.999999')),
                             axis=1)
df = df.drop(df[['date_shift-', 'date_shift+']], axis=1)
#Check 'user':
df['check_user'] = df.apply(lambda x: get_new_session_from_cat(x['user_id_shift-'],
                                                               x['user_id'],
                                                               x['user_id_shift+']),
                            axis=1)
df = df.drop(df[['user_id_shift-', 'user_id_shift+']], axis=1)
#Summarize checks:
df['session_bound'] = df['check_ts'] + df['check_pdate'] + df['check_user']
#print(df)
df = df.drop(df[['check_ts', 'check_pdate', 'check_user']], axis=1)
df = df[df['session_bound'] == True]

#Проверка датасета на наличие пользователей с незакрытой сессией (когда количество 'session_bound' нечетное)
#и удаление незакрытых сессий из датасета, последней при нечетном кол-ве 'session_bound':
even_check = df.groupby('user_id').agg(qty=('session_bound', 'count'))
even_users = list(even_check[even_check['qty'] % 2 == 1].index)
#list of indexes to remove from dataset:
to_drop = df[df['user_id'].isin(even_users)].groupby('user_id').tail(1).index.to_list()
#print(to_drop)
df = df.drop(to_drop, axis=0)
df = df.drop('session_bound', axis=1)
#Получение результ. таблицы со стартом и стопом каждой сессии:
df['end_ts'] = df['ts'].shift(-1)
#print(df)
result = df.iloc[::2].reset_index(drop=True)
#print(result)
result = result[['user_id', 'ab_group', 'ts', 'end_ts', 'pdate']]
result.rename(columns={'ts': 'start_ts'}, inplace=True)
#print(result)

#-------------------------------------TASK No.2-----------------------------------
AB = result.copy()
#print(f'AB = \n{AB}')
#group A:
mask_A = AB.loc[:, 'ab_group'] == 'A'
A = AB.copy()[mask_A]
#A = AB[AB['ab_group'] == 'A'] #this method will be deprecated
#print(A)
A['row_number'] = A.groupby('user_id').cumcount() + 1
#print(A)
#g_size = A.groupby('user_id').size().to_frame('size')
#print(g_size)
#A = A.join(g_size, on='user_id', how='left')
#print(f'Group A:\n{A}')
A = A[A['row_number'].isin([1, 2])]
#print(f'Group A only first two session:\n{A}')
A_sess_qty = A.groupby('row_number')['user_id'].count().to_frame('qty')
#print(f'Group A - Session Quantity:\n{A_sess_qty}')
print(f'Conversion A = {A_sess_qty.iloc[-1, 0] / A_sess_qty.iloc[0, 0]}')
#--------------------------------------------------------------------------------------
#group B:
mask_B = AB.loc[:, 'ab_group'] == 'B'
B = AB.copy()[mask_B]
B['row_number'] = B.groupby('user_id').cumcount() + 1
B = B[B['row_number'].isin([1, 2])]
#print(f'Group B only first two session:\n{B}')
B_sess_qty = B.groupby('row_number')['user_id'].count().to_frame('qty')
#print(f'Group B - Session Quantity:\n{B_sess_qty}')
print(f'Conversion B = {B_sess_qty.iloc[-1, 0] / B_sess_qty.iloc[0, 0]}')



