#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 13:22:32 2017

@author: wrk
"""


import sys
import math
from gurobipy import *
from log import *

lencommandline = len(sys.argv)

if lencommandline < 2:
    print('Usage: myguropi.py lpfilename [dual IIS]')
    exit(0)

log = Logger("mygurobi.log")    

method = -1  # -1=automatic, 0=primal simplex, 1=dual simplex, 2=barrier, 3=concurrent, 4=deterministic concurrent

getduals = 0
getIIS = 0

if lencommandline > 2:
    for j in xrange(2, lencommandline):
        if sys.argv[j] == 'dual':
            getduals = 1
        elif sys.argv[j] == 'IIS':
            getIIS = 1
        else:
            log.stateandquit("illegal command line option " + sys.argv[j] + "\n")


# Read and solve model

model = read(sys.argv[1])

model.params.Method = method
model.params.Presolve = 0
model.params.ScaleFlag = 0

#model.params.FeasibilityTol = 1e-5
if method == 2:
    model.params.Crossover = 0

log.joint('Solving %s\n' % sys.argv[1])
log.joint("variables = " + str(model.NumVars) + "\n")
log.joint("constraints = " + str(model.NumConstrs) + "\n")

    
model.optimize()

if model.status == GRB.status.INFEASIBLE:
    log.joint('->problem infeasible\n')
    if getIIS:
        model.computeIIS()
        iismodelname = "hey.ilp"
        model.write(iismodelname)
        log.joint("wrote IIS to " + iismodelname + "\n")
    log.closelog()
    sys.exit()

if model.status == GRB.status.UNBOUNDED:
    log.joint('->problem unbounded\n')
    if getIIS:
        model.computeIIS()
        iismodelname = "hey.ilp"
        model.write(iismodelname)
        log.joint("wrote IIS to " + iismodelname + "\n")
    log.closelog()
    sys.exit()
    
if model.status == GRB.status.INF_OR_UNBD:
    log.joint('->LP infeasible or unbounded\n')
    log.closelog()
    sys.exit()

log.joint('Optimal objective = %g\n' % model.objVal)

count = 0
for v in model.getVars():
    if math.fabs(v.x) > 0.0000001:
        count += 1

log.joint(str(count) + " nonzero variables in solution\n")
for v in model.getVars():
    if math.fabs(v.x) > 0.0000001:
        log.joint( v.varname + " = " +str(v.x) + "\n")

log.joint("bye.\n")
log.closelog()