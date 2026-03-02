degree_str, value_str = input().split()
degree, value = int(degree_str), float(value_str)

rate = []
derivative = 0
# print(degree, value)

for i in range(degree+1):
    rate.append(input())
# print(rate)

for i in range(len(rate)):
    # print(derivative)
    derivative = derivative + float(rate[i])*(len(rate)-i-1)*value**(len(rate)-i-2)
    # print('rate[i]',rate[i],'i',i,'len(rate)',len(rate),'derivative',derivative)

print(f"{derivative:.3f}")


