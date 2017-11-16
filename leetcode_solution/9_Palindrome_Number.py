class Solution:  
    # @return a boolean  
    def isPalindrome(self, x):  
        if x<0:  
            return False  
        div=1  
        while div<=x/10:  
            div*=10  
        while x>0:  
            if x/div!=x%10:  
                return False  
            x=(x%div)/10  
            div/=100  
        return True  