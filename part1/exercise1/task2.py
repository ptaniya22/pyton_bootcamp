numb=int(input())
isPalindrome=False
inv_numb=0
rest=0
razr=0
if numb>=0:
    temp=numb
    while temp!=0:    
        temp=temp//10
        razr+=1
#print(razr)
    razr=razr-1
    temp=numb
    while temp!=0:
    #print(inv_numb)
        inv_numb=inv_numb+(temp%10)*10**razr
        temp=temp//10
    #print(numb)
        razr-=1
        # print('inv_numb=',inv_numb)
        # print('numb=',numb)
    if inv_numb==numb:
        isPalindrome=True

print(isPalindrome)