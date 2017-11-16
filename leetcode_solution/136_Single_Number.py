# -*- coding: utf-8 -*-
class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        使用异或运算符解决
        <两个相同的数进行按位异或运算结果一定为0，一个数与0按位异或结果即为该数本身>
        """
        res = 0
        for i in nums:
            print res,bin(res)[2:]
            res ^= i
            
        return res

t = Solution()
print t.singleNumber([1,3,5,3,5,1,7])