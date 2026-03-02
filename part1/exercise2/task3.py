#len(matrix) количество строк (rows)
#len(matrix[i]) количество столбцов (cols) в строке i
matrix = []

with open("input.txt") as f:
    for line in f:
        row = list(map(int, line.split()))
        matrix.append(row)        

# print('*****matrix*****',matrix)


def count_square(matrix):

    rows = len(matrix)
    cols = len(matrix[0])
    # print('cols',cols)
    count = 0
    found = False
    Err =  False

    for i0 in range(rows):    
        for j0 in range(cols):
            Err =  False
            if matrix[i0][j0]!=1:
                continue
            if i0 > 0 and matrix[i0-1][j0] == 1:
                continue
            if j0 > 0 and matrix[i0][j0-1] == 1:
                continue

            # print('new i0,j0=',i0,j0)
            size_i = 0
            while j0 + size_i < cols and matrix[i0][j0 + size_i] == 1:
                size_i += 1
            size_j = 0
            while i0 + size_j < rows and matrix[i0 + size_j][j0] == 1:
                size_j += 1
            # print('size_i,size_j=',size_i,size_j)

            if (size_i != size_j) or (size_i == 1):
                # print('error off size')
                continue
            
            ok=True
            for i in range(i0, i0 + size_i):
                for j in range(j0, j0 + size_i):
                    if matrix[i][j] != 1:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                continue

    # FRAMES
            top = i0 - 1
            bottom = i0 + size_i
            left = j0 - 1
            right = j0 + size_i

    # TOP
            if top >= 0:
                # print('top frame')
                for j in range(j0, right):
                    if matrix[top][j] != 0:
                        Err=True
                        # print('Err in top frame')
                        break
                    # if Err:
                        # break

    # LEFT
            # print('Err status after top frame is ',Err)
            if not Err and left >= 0:
                # print('left frame')
                for i in range(i0,bottom):
                    if matrix[i][left] !=0:
                        Err=True
                        # print('Err in left frame')
                        break
            # print('Err status after left frame is ',Err)

    # RIGTH
            if not Err and right<cols:
                for i in range(i0,bottom):
                    if matrix[i][right] !=0:
                        Err=True
                        # print('Err in rigth frame')
                        break
            # print('Err status after rigth frame is ',Err)

    # BOTTOM
            if not Err and bottom<rows:
                for j in range(j0,right):
                    if matrix[bottom][j] !=0:
                        Err=True
                        # print('Err in bottom frame')
                        break
            # print('Err status after bottom frame is ',Err)


            if not Err:
                count += 1
            
            if not Err and count>0:
                for i in range(i0,i0+size_i):
                    for j in range(j0,j0+size_i):
                        matrix[i][j]=0

           
    # print(matrix)
    # print('count of square=',count)

    return count

def count_circle(matrix):
    found=False
    count=0
    rows = len(matrix)
    cols = len(matrix[0])

    for i0 in range(rows): 
        cols = len(matrix[i0])    
        for j0 in range(cols):
            # if j0 >= cols:       
            #     break
            #     Err =  False
            # print('i0= ',i0,'j0= ',j0)
            if matrix[i0][j0]!=1:
                continue
            if i0 > 0 and matrix[i0-1][j0] == 1:
                continue
            if j0 > 0 and matrix[i0][j0-1] == 1:
                continue
            

            Err = False
            D = 0
            D2 = 0
            L_top = 0
            R = 0
            med_i = 0
            med_j = 0
            j_temp = 0
            

            # print('new i0,j0=',i0,j0)
            
            # print('rows=',rows)

            for i in range(i0,len(matrix)):    
                if matrix[i][j0]==1:
                    D+=1
                else:
                    # print('i= ',i,'cols=',len(matrix[i]))
                    found=False
                    break
            if D==1:
                continue


            # print('D=',D)
            if D%2==1:
                R=D//2+1
            else:
                R=int(D/2)
            # print('R=',R)

            L_top=0
            for j in range(j0,len(matrix[i0])):
                # print('i0= ',i0,'j= ',j,'L_top= ',L_top,"val =", matrix[i0][j])
                if matrix[i0][j]==1:
                    L_top+=1
                else:
                    break

            if i0 > 0:
                for j in range(j0,j0+L_top+2):
                    if j >= cols:        
                        break
                    # print('Checking new i0 j0 as candidat')
                    if matrix[i0-1][j] != 0:
                        Err = True
                        break


            if not Err:
                # print('***part1***')
                pos=0
                for i in range(i0,i0+int((D-L_top)/2)):
                    # print('pos=',pos,'i=',i)
                    # med_i=i
                    for j in range(j0-pos,j0+L_top+pos):
                        med_j=j0-pos
                        if j>len(matrix[i])-1 or matrix[i][j]!=1 or (matrix[i][j0-pos-1]!=0 or ((j0+L_top+pos)<cols and matrix[i][j0+L_top+pos]!=0)):
                            # print("len(matrix[i]) =",len(matrix[i])-1, "  i =", i,"  j =", j, "val =", matrix[i][j])
                            Err=True
                            # print('Err=',Err)
                    if Err:
                        # print('Err part1')
                        break
                    else:
                        pos+=1
                med_i=i0+int((D-L_top)/2)
                # print('med_j= ', med_j, 'cols= ',cols)
                
            for j in range(med_j-1,cols):
                # print('j', j, 'val= ', matrix[med_i][j])
                if matrix[med_i][j]==1:
                    D2+=1
                else:
                    break
            
            # print('D= ',D,'D2= ',D2, 'Error status is ', Err)

            if D!=D2:
                Err=True
                # print('Error!Figure is not Circle')
                    

            if not Err:
                # print('****part2***')
                # print(L_top)
                for i in range(med_i,med_i+L_top):
                    # print("i =", i, "j =", j, "val =", matrix[i][j])
                    for j in range(med_j-1,D+med_j-1):
                        # print("len(matrix[i]) =",len(matrix[i])-1, "  i =", i,"  j =", j, "val =", matrix[i][j])
                        # print("  j =", j, "val =", matrix[i][j])
                        if j>len(matrix[i])-1 or matrix[i][j]!=1:
                            # print("len(matrix[i]) =",len(matrix[i])-1,"  i =", i, "  j =", j, "val =", matrix[i][j])
                            Err=True
                            # print('Err_part2=',Err)
                    if Err:
                        # print('Err part2')
                        break

            if not Err:
                # print('***part3***')
                # print(Err)
                pos=0
                # print('L_top= ',L_top, 'med_i= ',med_i,'medj= ', med_j,'pos= ',pos)
                for i in range(med_i+L_top,i0+D):
                    # print("len(matrix[i]) =",len(matrix[i])-1, "i = ", i,"  j =", j, "val =", matrix[i][j])
                    for j in range(med_j+pos,D+med_j-2-pos):
                        # print("len(matrix[i]) =",len(matrix[i])-1, "i = ", i,"  j =", j, "val =", matrix[i][j])
                        if j>len(matrix[i])-1 or matrix[i][j]!=1 or (matrix[i][med_j+pos-1]!=0 or matrix[i][med_j+D-pos-2]!=0) :
                            # print("len(matrix[i]) =",len(matrix[i])-1, "i = ", i," j =", j, "val =", matrix[i][j])
                            Err=True
                            # print('Err=',Err)
                    if Err:
                        # print('Err part3')
                        break
                    else:
                        pos+=1

            ###### FRAMES ######
            top = i0 - 1 


            # print('Err status after bottom frame is ',Err)
            if not Err:
                count += 1
        # print('Err=',Err)
                # print('count=',count)  

            if not Err and count>0:
                # ********PART1 ZEROING******
                pos=0
                for i in range(i0,i0+int((D-L_top)/2)):
                    # pos+=1
                    # print('pos=',pos,'i=',i)
                    for j in range(j0-pos,j0+L_top+pos):
                        matrix[i][j]=0
                    pos+=1

                # ********PART2 ZEROING******
                for i in range(med_i,med_i+L_top):
                    for j in range(med_j-1,D+med_j-1):
                        matrix[i][j]=0

                # ********PART3 ZEROING******
                pos=0
                for i in range(med_i+L_top,i0+D):
                    for j in range(med_j+pos,D+med_j-2-pos):
                        matrix[i][j]=0
                pos+=1
            D=0
            D2=0
            

    # print(matrix)
    # print('count of circle=',count) 
    return count

print(count_square(matrix), count_circle(matrix))
