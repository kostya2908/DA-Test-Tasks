import numpy as np

a = [1,2,3,4,5,6,7,8,9]
#a = np.arange(1000000000).tolist()
#print(a)


#FIRST:

first = a[::-1]
#print(f'first:\n{first}')


#SECOND:

left = 0
right = len(a) - 1
second = a.copy()
while left < right:
    temp = second[left]
    second[left] = second[right]
    second[right] = temp
    left += 1
    right -= 1
#print(f'second:\n{second}')


#THIRD:

third = []
for i in a:
    third.insert(0, i)
print(f'third:\n{third}')

