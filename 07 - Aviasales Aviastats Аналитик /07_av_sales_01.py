import pandas as pd
import json
import hashlib

def get_hash(a, b):
    return hashlib.md5((a + str(b)).encode('utf-8')).hexdigest()

def get_route(lst):
    tmp = [lst[0].get('origin', 'no_data')]
    for i in lst:
        tmp.append(i.get('destination', 'no_data'))
    route = '-'.join(tmp)
    return route 

#pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

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
print(result.columns)
result = result[cols]
print(result.columns)
print(result.head(300))
#print(result[result['flights_count'] > 1].iloc[:, [0,5,6,7,8,9,10,11]].head(10))

