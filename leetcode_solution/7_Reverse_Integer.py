class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        if(abs(x) > pow(2,31)-2):
            return 0;
        else:
            if x>0:
                strx = str(x)
                str_reverse_x = strx[::-1]
                return int(str_reverse_x)
             
            elif (x == 0):
                    return 0
            else:
                nega_x = -x
                str_x = str(nega_x)
                return(-int(str_x[::-1]))
                 
 
s= Solution()
print s.reverse(123)
