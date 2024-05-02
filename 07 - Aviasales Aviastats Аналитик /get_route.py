def get_route(lst):
    tmp = [lst[0].get('origin')]
    print(tmp)
    for i in lst:
        print(f'i = {i}')
        tmp.append(i.get('destination'))
        print(f'tmp = {tmp}')
    route = '-'.join(tmp)
    print(route)


a = [{'origin': 'SVO', 'destination': 'MCT', 'airline': 'WY', 'baggage': 'With baggage'}, {'origin': 'MCT', 'destination': 'HKT', 'airline': 'WY', 'baggage': 'With baggage'}]
get_route(a)
