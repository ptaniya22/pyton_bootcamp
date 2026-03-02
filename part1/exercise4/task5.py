flag_sign = False
flag_negativ = False
flag_point = False
point = 0
count_point = 0
Err = False
is_digit = True
int_str = 0
fract_str = 0
int_part = 0
fract_part = 0
code_symb = 0
temp = 0


S = input()
# strip deleted all ' '
S = S.strip()
#***********CHECKING SIGN
if S[0] == '-':
    flag_sign = True
    flag_negativ = True
if S[0] == '-' or S[0] == '+':
    S = S[1:len(S)]
    flag_sign = True
# print("S= ",S)

point = S.find('.')
# print(S,point)
count_point = S.count(".")
# print(S,count_point)
if count_point > 1:
    Err = True
    print("Error of typing. More '.'")
   


if point >= 0:
    int_str = S[0:point]
    fract_str = S[point+1:len(S)]
else:
    int_str = S
    fract_str = '0'
# print('Part string before . is',int_str, 'Part string after .  is ',fract_str)

# print("S= ",S)
# is_digit = S.isdigit()
# print('is_digit',is_digit)
if not int_str.isdigit() or not fract_str.isdigit():
    Err = True
    print("Error of typing.Letter in number ")


def strig_to_int(str):
    numb = 0
    for i in range(len(str)):
        code_symb = ord(str[i]) - ord('0')
        numb = numb + code_symb*10**(len(str)-i-1)   
    return numb

def strig_to_fract(str):
    numb = 0
    for i in range(len(str)):
        code_symb = ord(str[len(str)-i-1]) - ord('0')        
        numb = numb + code_symb/10**(len(str)-i)              
    return numb

# temp = strig_to_int(int_str)
if not Err:
    temp = 2*(strig_to_int(int_str) + strig_to_fract(fract_str))
    if flag_negativ:
        temp = temp*(-1)
# print('result of function',temp)

    print(f"{temp:.3f}")


# print('Type of ineger part is ',type(int_part),'Ineger part is ', int_part)
# print('Status off error is ',Err)

