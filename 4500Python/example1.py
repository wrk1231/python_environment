import gurobipy
from gurobipy import *

try:

    # Create a new model
    m = Model("example1")

    # Create variables (lowerbound of 0 by default)
    x1 = m.addVar(vtype=GRB.CONTINUOUS, name="x1", lb=0)
    x2 = m.addVar(vtype=GRB.CONTINUOUS, name="x2", lb=0)
    x3 = m.addVar(vtype=GRB.CONTINUOUS, name="x3", lb=0)

    # Integrate new variables
    m.update()

    # Set objective
    m.setObjective(110*x1 + 240*x2 + 340*x3, GRB.MAXIMIZE)

    # Add constraint: 10x1 + 25x2 + 30x3 <= 35
    m.addConstr(10*x1 + 25*x2 + 30*x3 <= 35, "c0")

    # Optimize (model is updated when we optimize)
    m.optimize()

    #print model status (2 is optimal)
    #https://www.gurobi.com/documentation/6.5/refman/optimization_status_codes.html
    print 'Model status:', m.status

    #print decision variables
    for v in m.getVars():
        print v.varName, v.x

    #print objective function value
    print 'Obj:', m.objVal

except GurobiError:
    print 'Error reported'
    





    