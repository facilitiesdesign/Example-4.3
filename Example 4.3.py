# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 10:22:03 2022

@author: grace_elizabeth
"""

from gurobipy import *

try:
    
    M = 100000
    
    #Create lists
    nodes = ['F1', 'F2', 'T1', 'T2', 'T3', 'C1', 'C2']
    net_flow = [900, 600, 0, 0, 0, -750, -750]
    cost = [ # F1, F2, T1, T2, T3, C1, C2
        [M, M, 8, 11, 5, M, M], #F1 
        [M, M, 12, 8, 5, M, M], #F2 
        [8, 12, M, M, M, 6, 3], #T1 
        [11, 8, M, M, M, 12, 1], #T2 
        [5, 5, M, M, M, 9, 19], #T3 
        [M, M, 6, 12, 9, M, M], #C1 
        [M, M, 3, 1, 19, M, M] #C2
        ]
    capacity = [ # F1, F2, T1, T2, T3, C1, C2
        [0, 0, 500, 1500, 350, 0, 0], #F1 
        [0, 0, 1200, 750, 450, 0, 0], #F2 
        [500, 1200, 0, 0, 0, 1000, 150], #T1 
        [1500, 750, 0, 0, 0, 750, 200], #T2 
        [350, 450, 0, 0, 0, 1000, 1500], #T3 
        [0, 0, 1000, 750, 1000, 0, 0], #C1 
        [0, 0, 150, 200, 1500, 0, 0] #C2
        ]    
    
    #indices
    n = len(nodes)
        
    #Create model
    m = Model("Example 4.1")
        
    #Declare variable
    x = m.addVars(n, n, lb = 0, vtype = GRB.CONTINUOUS, name = "flow")
        
    #Set objective fuction
    m.setObjective(quicksum(cost[i][j] * x[i,j] for i in range(n) for j in range(n)), GRB.MINIMIZE)
        
    #Write constraints
    for i in range(n):
        m.addConstr(quicksum(x[i,j] for j in range(n)) - quicksum(x[j,i] for j in range(n)) == net_flow[i], name = "4.22")
        
    for i in range(n):
        for j in range(n):
            m.addConstr(x[i,j] <= capacity[i][j], name = "4.23")
                
    #Call Gurobi Optimizer
    m.optimize()
    if m.status == GRB.OPTIMAL:
        for v in m.getVars():
            if v.x > 0:
                print('%s = %g' % (v.varName, v.x)) 
        print('Obj = %f' % m.objVal)
    elif m.status == GRB.INFEASIBLE:
        print('LP is infeasible.')
    elif m.status == GRB.UNBOUNDED:
        print('LP is unbounded.')
except GurobiError:
    print('Error reported')