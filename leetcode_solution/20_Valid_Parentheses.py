# -*- coding: utf-8 -*-
class Stack(list):
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)
def matches(open,close):
    opens = "([{"
    closers = ")]}"
    return opens.index(open) == closers.index(close)
class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        题目理解有问题
        """
#         judge = True
#         if(len(s)%2 == 1):
#             judge = False
#         elif (s[0] == ')' or s[0]==']' or s[0]== '}'):
#             judge = False
#         elif (s[-1] == '(' or s[0]=='{' or s[0]=='['):
#             judge = False 
#         else:
#             for i in range(len(s)-1):
#                 if (s[i] == '('):
#                     if(s[i+1] != ')'):
#                         judge = False
#                 elif (s[i] == '['):
#                     if(s[i+1] != ']'):
#                         judge = False
#                 elif (s[i] == '{'):
#                     if(s[i+1] != '}'):
#                         judge = False
#              
#             for i in range(len(s)-1,0,-1):
#                 if (s[i] == ')'):
#                     if(s[i-1] != '('):
#                         judge = False
#                 elif (s[i] == ']'):
#                     if(s[i-1] != '['):
#                         judge = False
#                 elif (s[i] == '}'):
#                     if(s[i-1] != '{'):
#                         judge = False
#         
#         return judge
        temp_str = Stack()
        balanced = True
        index = 0
        while index < len(s) and balanced:
            symbol = s[index]
            if symbol in "([{":
                temp_str.push(symbol)
            else:
                if temp_str.isEmpty():
                    balanced = False
                else:
                    top = temp_str.pop()
                    if not matches(top,symbol):
                           balanced = False
            index = index + 1
        if balanced and temp_str.isEmpty():
            return True
        else:
            return False


t = Solution()
print t.isValid('()')