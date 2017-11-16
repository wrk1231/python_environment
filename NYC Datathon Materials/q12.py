# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pandas import DataFrame,Series
venues_data2 = pd.read_csv('output.csv')
del venues_data2['Unnamed: 0']


venues_data = pd.read_csv('venues.csv')
collect_types = []
venues_data['copy_types'] = [None]*267958

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
            
collect_types.append('idnum') 
    
venues_data = pd.read_csv('venues.csv')
venues_data['idnum'] = range(267958)
venues_data2['idnum'] = range(267958)

