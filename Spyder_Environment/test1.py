#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 17:01:14 2017

@author: wrk
"""

import pandas as pd
import numpy as np
from scipy.stats import norm
from statsmodels.tsa.stattools import acf

def autocoef(data,k):
    m = np.mean(data)
    n = len(data)
    return np.nansum((data[:n-k] - m)*(data[k:] - m))/np.nansum((data-m)**2)
# =============================================================================
#     return np.nansum((data[:(n-k)]-m)*(data[k:]-m))/np.nansum((data-meanw)**2)/(n-k)
# =============================================================================
test_data = np.random.normal(5,1,100)
print(test_data.mean())

res = np.array([autocoef(test_data,i) for i in range(10)]) - acf(test_data,nlags=10)[9]
print(res)