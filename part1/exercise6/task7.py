N, M = map(int, input().split())

matrix = []

for i in range(N):
    while True:
        row = list(map(int, input().split()))
        
        if len(row) == M:
            matrix.append(row)
            break   
        else:
            print("Error!Number of elements is not equal M!")


temp=0
for j in range(M):
    matrix[0][j]=temp+matrix[0][j]
    temp=matrix[0][j]

temp=0
for i in range(N):
   matrix[i][0]=temp+matrix[i][0]
   temp=matrix[i][0]

for i in range(1,N):
    for j in range(1,M):
        matrix[i][j]=matrix[i][j]+max(matrix[i-1][j],matrix[i][j-1])

# for row in matrix:
#     print(row)

print(matrix[N-1][M-1])