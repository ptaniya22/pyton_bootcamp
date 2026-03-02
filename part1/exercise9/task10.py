# N, T = map(int,input().split())
# print(N,T)

min_cost = None
total_cost = 0

try:
    str_NT = input().split()
    
    if len(str_NT) != 2:
        print("error!Incorrect number of elements")
        exit()
        
    N, T = map(int, str_NT)
    
    if N <= 0 or T <= 0:
        print("error!incorrect dates N and T")
        exit()

    Apparats = {}

    for _ in range(N):
        str_year_cost_time = input().split()

        if len(str_year_cost_time) != 3:
            print("error!Incorrect number of elements")
            exit()
        year, cost, time = map(int, str_year_cost_time)

        if year <= 0 or cost <= 0 or time <= 0:
            print("error!incorrect dates")
            exit()
    
        if year not in Apparats:
            Apparats[year] = []
    
        Apparats[year].append((cost, time))

# print(Apparats)
except ValueError:
    print("error of typing")
    exit()

for year in Apparats:
    Apparats_list = Apparats[year]

    if len(Apparats_list) < 2:
        continue
    
    for i in range(len(Apparats_list)):
        for j in range(i + 1, len(Apparats_list)):
            cost1, time1 = Apparats_list[i]
            cost2, time2 = Apparats_list[j]
            
            if (time1 + time2) >T:
                continue

            total_cost = cost1 + cost2
            if min_cost is None or total_cost < min_cost:
                min_cost = total_cost
                    
                
            # print('[year]= ',year,'i= ',i,'j= ',j, cost1+cost2,'time= ',time1 + time2)
        

if min_cost is None:
    print("error")
else:
    print(min_cost)