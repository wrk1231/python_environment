# -*- coding: utf-8 -*-

import cvxpy as cvx
import numpy as np

#define the data
numassets = 4;
numscenarios = 3;
S = np.mat([[0.2,0.5,1.0],
                [1.0,1.2,0.2],
                [0.1,1.0,1.3],
                [0.5,0.8,1.2]]).transpose();
print type(S)