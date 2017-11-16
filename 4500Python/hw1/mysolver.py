#!/usr/bin/python

import sys
import math
from gurobipy import *

def lpsolver(lpfilename, logfilename):

    print "solving LP in file", lpfilename, "with log file", logfilename
    try:
        log = open(logfilename,"w")    
    except IOError:
        print ("Cannot open log file %s\n" % logfilename)
        return 0
    # Read and solve model

    log.write("will try to read LP file at" + lpfilename)

    model = read(lpfilename)
    model.optimize()

    log.write('now solving LP\n')
    log.write("variables = " + str(model.NumVars) + "\n")
    log.write("constraints = " + str(model.NumConstrs) + "\n")

    if model.status == GRB.status.INF_OR_UNBD:
        print "->LP infeasible or unbounded"
        log.write('->LP infeasible or unbounded\n')
        log.close()
        return 0

    log.write('Optimal objective = %g\n' % model.objVal)

    count = 0
    for v in model.getVars():
        if math.fabs(v.x) > 0.0000001:
            count += 1

    log.write(str(count) + " nonzero variables in solution\n")
    var=[]
    for v in model.getVars():
        if math.fabs(v.x) > 0.0000001:
            print( v.varname + " = " +str(v.x))
            log.write( v.varname + " = " +str(v.x) + "\n")
            var.append(v.x)
    log.write("bye.\n")
    log.close()

    if model.objVal<0:
        return var
    else:
        return 0
