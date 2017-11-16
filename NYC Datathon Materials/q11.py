# -*- coding: utf-8 -*-

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
venues_data2 = pd.read_csv('output.csv')

venues_data = pd.read_csv('venues.csv')
del venues_data['id']
venues_data['copy_types'] = [None]*267958
collect_types = []
collect_types.append('id')
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

venues_data2.columns = collect_types

venues_data2.to_csv('output_2.csv')