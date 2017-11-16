#!/usr/bin/python

import sys
from arbwriter import writelp
from mysolver import lpsolver
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import *
import random
# import matplotlib
# from matplotlib import *
# import matplotlib.pyplot as plt
import numpy as np

if len(sys.argv) != 3:
    sys.exit("usage: arbtest.py datafilename lpfilename\n")

#now open and read data file
try:
    datafile = open(sys.argv[1], 'r') # opens the data file
except IOError:
    sys.exit("Cannot open file %s\n" % sys.argv[1])


lines = datafile.readlines();
datafile.close()

#print lines[0]
firstline = lines[0].split()
#print "first line is", firstline

numsec = int(firstline[1])
numscen = int(firstline[3])
r = float(firstline[5])
# print "\n"
# print "number of securities:", numsec,"number of scenarios", numscen,"r",r
# print "\n"

#allocate prices as one-dim array
p = [0]*(1 + numsec)*(1 + numscen)
k = 0
# line k+1 has scenario k (0 = today)
while k <= numscen:
    thisline = lines[k + 1].split()
#    print "line number", k+1,"is", thisline
    # should check that the line contains numsec + 1 words
    j = 1
#    print "scenario", k,":"
    p[k*(1 + numsec)] = 1 + r*(k != 0)
    while j <= numsec:
        value = float(thisline[j])
        p[k*(1 + numsec) + j] = value
#        print " sec ", j, " -> ", p[k*(1 + numsec) + j]
        j += 1
    k += 1


#now write LP file, now done in a separate function (should read data this way, as well)

###################### trial ######################
    
lpwritecode = writelp(sys.argv[2], p, numsec, numscen)
#now solve lp 

lpsolveposition = lpsolver(sys.argv[2], "test.log")
hist=[]
large = 0
small = numscen
for a in range(100):
        sum_error=0
        k = 1
        while k <= numscen:
            scen_test=p[k*(1 + numsec)]*lpsolveposition[0]
            j = 1
            while j <= numsec:
                value2=p[k*(1 + numsec) + j]
                rand=random.uniform(-5*value2,5*value2)
                scen_test+=(value2+rand/100)*lpsolveposition[j]
                j += 1
            if scen_test < 0:
                sum_error+=1
            k += 1
        if sum_error > large:
                large = sum_error
        if sum_error < small:
                small = sum_error
        hist.append(sum_error)
outcome=np.array(hist)
histogram=np.histogram(outcome,bins=[i for i in range(small, large + 1)])
plt.hist(outcome,bins=[i for i in range(small, large + 1)])
plt.title('Histogram of failed scenarios under the price volatility of 5%')
plt.show()
print '#######The distribution and bin of the histogram######## \n',histogram

