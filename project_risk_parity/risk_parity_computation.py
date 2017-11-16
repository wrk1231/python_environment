# -*- coding: utf-8 -*-
'''
@author: Ruikang Wang
'''
import sys
sys.path.append('..')
sys.path.append('../..')
import GC_risk_parity 
from GC_risk_parity import *
import risk_parity_data
from risk_parity_data import *

import numpy as np
import pandas as pd
from pandas import *
from pandas import DataFrame
from pandas import Series
import scipy
from scipy import optimize
from scipy.optimize import minimize
import math
from pandas.tslib import Timestamp
from datetime import datetime


CP = pd.DataFrame(pd.read_csv('data_original.csv'))
CP.index = CP['date']
CP = CP.drop(['date'],axis = 1)
cur_len = len(CP)
data = []

## set your backtest frequency: f_month for monthly and f_quarter for quarterly
freq = f_month 

times =  int(cur_len/f_month)

for x in range(times):
    temp = CP.iloc[freq*x:freq*(x + 1)]
    data.append(np.matrix(temp))

record = [] ## record results of each optimize
for x in range(times):
    Cov_matrix = np.cov(data[x])
    sigma = []
    for i in range(Num_of_assets):
        sigma.append ( Cov_matrix[i][i] )
        
        
    def fun(w):
 ## w = [w0,w1,w2,w3,w4,w5,w6] w_matrix: turn w into matrix
        w_matrix = np.matrix(w)
        p = [None] * Num_of_assets
        Sigma =  w_matrix * Cov_matrix * w_matrix.T
        for i in range(Num_of_assets):
            add = 0   
            for j in range(Num_of_assets):        
                add += w[j]*w[i]*sigma[j]*sigma[i]    
            p[i] = add/(Sigma)
    ## p[i] = risk contribution ratio for each stock_i

    ## our goal: minimize f:
        #minimize_solve = (p[0] + p[1] + p[2] + p [3] + p[4] + p[5] + p[6] - 1)**2
        minimize_solve = ((p[0] + p[1] +p[2] -(p[3]+[4]))**2 + (p[3] + p[4] - (p[5]+p[6]))**2 + (p[0]+p[1]+p[2]-(p[5]+p[5]))**2)
        return minimize_solve
    
    
    def constrain_sum_of_ratio(w):
    
        total_sum = 0.0

        for i in range(Num_of_assets):
            total_sum += float(w[i])

            total_sum = float(total_sum - 1.0)

        return total_sum

    weight_init = [w0, w1, w2, w3, w4, w5, w6]
    bnds = (b0,b1,b2,b3,b4,b5,b6)
    cons = ({'type': 'eq', 'fun': constrain_sum_of_ratio})
    
    res = minimize(fun, weight_init, method='L-BFGS-B', bounds=bnds,constraints=cons)
    record.append(res.x)