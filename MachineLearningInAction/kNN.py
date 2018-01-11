# -*- coding: utf-8 -*-
import numpy
from numpy import matrix
from numpy import *
import operator

def createDataSet(): 
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]]) 
# =============================================================================
#     print group
# =============================================================================
    labels = ['A','A','B','B']
    return group, labels

def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1])) 
        index += 1
    return returnMat,classLabelVector


