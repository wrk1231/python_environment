# -*- coding: utf-8 -*-
'''
@author: Ruikang Wang
'''

import sys
sys.path.append('..')
sys.path.append('../..')
import GC_risk_parity 
from GC_risk_parity import *

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
