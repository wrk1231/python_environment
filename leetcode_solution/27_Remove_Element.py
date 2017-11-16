# class Solution:  
#     # @param    A       a list of integers  
#     # @param    elem    an integer, value need to be removed  
#     # @return an integer  
#     def removeElement(self, A, elem):  
#         index = 0  
#         for num in A:  
#             if num != elem:  
#                 A[index] = num  
#                 index += 1  
#                
#         return index  
# t = Solution()
# print type(t.removeElement([1,1,2,3,3,4], 3))
class Solution:  
    # @param    A       a list of integers  
    # @param    elem    an integer, value need to be removed  
    # @return an integer  
    def removeElement(self, A, elem):  
      
              
        return A.__len__() - A.count(elem)  
t = Solution()
print t.removeElement([1,1,2,3,3,4], 3)