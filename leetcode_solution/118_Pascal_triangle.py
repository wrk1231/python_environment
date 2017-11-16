class Solution(object):
    def generate(self, numRows):
        """
        :type numRows: int
        :rtype: List[List[int]]
        """
        if numRows == 0:
            return []
        else:
            r_list = [[1]]
            while(numRows > 1):
                a = [1]
                for i in range(len(r_list[-1]) - 1):
                    a.append(r_list[-1][i] + r_list[-1][i+1])
                a.append(1)
                r_list.append(a)
                numRows -= 1
            
            return r_list

t = Solution()
print t.generate(5)
                
        