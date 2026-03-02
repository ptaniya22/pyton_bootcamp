N = int(input())

numb_list = []
temp = 0
found = False
count = 1

for i in range(N):
    numb_list.append(input())

# print(numb_list)
data =[numb_list[0]]

for i in range(N):
    if numb_list[i] not in data:
        count += 1
        data.append(numb_list[i])

print(count)