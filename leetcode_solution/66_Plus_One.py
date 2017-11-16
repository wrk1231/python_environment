class Solution(object):
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        res = 0
        resList = []
        for i in range(digits.__len__()):
            res += digits[i]* pow(10,len(digits) - i - 1)
        res += 1
        while(1):
            if res == 0:
                break
            else:
                 resList.append(res%10)
                 res = res/10
        
        return list(reversed(resList))
t = Solution()
print t.plusOne([-1,2,3])