# -*- coding: utf-8 -*-

import kNN
import matplotlib
groups,labels = kNN.createDataSet()

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0] ## get the num of rows
    diffMat = tile(inX,(dataSetSize,1)) - dataSet ## get the diff
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5  ## get the distance
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k): 
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


print classify0([0,0],groups,labels,3)