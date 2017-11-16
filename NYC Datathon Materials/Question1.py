#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 08:43:53 2017

@author: wrk
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pandas import DataFrame,Series
venues_data = pd.read_csv('venues.csv')
del venues_data['id']
#venues_data.info()
collect_types = []
venues_data['copy_types'] = [None]*267958
ans = []
origin_type = []

for i in range(len(venues_data['types'])):
    x = venues_data.loc[i,'types']
    x = x.strip('[')
    x = x.strip(']')
    x = x.strip('"')
    x = x.replace('\'','')
    x = x.replace(' ','')
    y = x.split(',')
    
    print i
    for s in y:
        if s not in collect_types:
            collect_types.append(s)
    origin_type.append(y)

df_collect = DataFrame(collect_types)
df_collect.to_csv('collection.csv')
#for y in origin_type:
#    temp = [1 if att in y else 0 for att in collect_types]
#    ans.append(temp)                
#
#output = DataFrame(ans)
#output.to_csv('output.csv')
#for x in collect_types:
#    venues_data[x] = [0]*267958
#
#print 'done'
#for i in range(len(venues_data['copy_types'])):
#    print i
#    c = venues_data['copy_types'][i]
#    for s in c:
#        
#        venues_data[s][i] += 1
#venues_data.to_csv('out.csv')                  
#    
    
#    
    
#print(venues_data['types'])
# new_york_venues_data = 