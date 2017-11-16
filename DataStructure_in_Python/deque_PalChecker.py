import deque_Class
from deque_Class import Deque
import pandas

def palchecker(astr):
    de = Deque()

    judge = True
    for x in astr:
        de.addRear(x)
  
    
    while de.size() >1 and judge:
        if de.removeFront() != de.removeRear():
        	judge = False
        	break

    return judge

            
t = '12321'

print palchecker(t)