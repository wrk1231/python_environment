import stack1
from stack1 import Stack
def getBinary_num(num,base):
    s = Stack()
     
    while(num > 0):
        a = num%base
         
        s.push(a)
        num = num/base
     
    st = ""
    while not s.isEmpty():
        st += str(s.pop())
        
    return st
 
print getBinary_num(7,2)


# def divideBy2(decNumber):
#     remstack = Stack()
# 
#     while decNumber > 0:
#         rem = decNumber % 2
#         remstack.push(rem)
#         decNumber = decNumber // 2
# 
#     binString = ""
#     while not remstack.isEmpty():
#         binString = binString + str(remstack.pop())
# 
#     return binString
# 
# print(divideBy2(42))

