 # -*- coding: utf-8 -*-
# def fact(n):  
#     if n == 0:  
#         return 1  
#     else:  
#         return n*fact(n-1)  
# 
# def Cnk0(n,m):  
#     return fact(n)/(fact(n-m)*fact(m))  
# 
# class Solution(object):
#       阶乘求二项式系数会超出int的界报错 故不能直接求
#     def generate(self, numRows):
#         """
#         :type numRows: int
#         :rtype: List[List[int]]
#         """
#         if numRows == 0:
#             return []
#         elif numRows == 1:
#             return [1]
#         
#         else:
#             a = [(Cnk0(numRows,k)) for k in range (0,numRows+1,1)]
#            
#             
#             return a
class Solution(object):
      
    def generate(self, numRows):
        """
        :type numRows: int
        :rtype: List[List[int]]
        """
        res = [1,1]
        if numRows == 0:
            return []
        elif numRows == 1:
            return [1]
        
        else:
            while(numRows >1):
                a = []
                a.append(1)
                for i in range(len(res)-1):
                    a.append(res[i] + res[i+1])
                a.append(1)
                res = a
                numRows -= 1
            
            return a
t = Solution()
print t.generate(6)
                
        