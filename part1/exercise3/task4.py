try:
    N = int(input())
    if N <= 0:
        print("Natural number was expected")
except ValueError:
    print("Natural number was expected")
    exit() 

matrix = []

for i in range(N):
    row = []               
    for j in range(i+1):
        if (i==0 and j==0) or (j==0 or j==i):
            row.append(1)
        else:
            row.append(matrix[i-1][j]+matrix[i-1][j-1])  
        
                
    matrix.append(row)     

# for row in matrix:
#     print(row)

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        print(matrix[i][j], end=' ')
    print()
    

