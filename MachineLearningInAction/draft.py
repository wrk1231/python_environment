# -*- coding: utf-8 -*-
import numpy
from numpy import *
import operator


def createDataSet(): 
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]]) 
# =============================================================================
#     print group
# =============================================================================
    labels = ['A','A','B','B']
    return group, labels
a,b = createDataSet()
c = a.sum(axis = 1)
print len(a)
d = zeros((4,3))
index = 0
d[1] =[1,2,3]
