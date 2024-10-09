"""
Author: Roger X. Lera Leri
Date: 2024/07/08
"""
from docplex.mp.model import Model
import numpy as np

def sol(x):

    ind = []
    for i in x.keys():
        if x[i].solution_value >= 0.9:
            ind += [i]
    return ind

def hitting_sets_problem(H:list,max_solve_time=60.0,n_threads=1):
    """
        This function solves the Hitting Sets Problem (HSP) problem
        forced_constraints: constraints to be satisfied: y_i = 0
    """
    if len(H) == 0:
        return []
    el = []
    for S in H:
        el += S
    el = np.unique(el)
    

    mdl = Model()
    # defining variables
    x = mdl.binary_var_dict(el,name='x') # a binary var for each element

    # defining constraints
    for S in H:
        lhs = [x[s] for s in S] # every element
        mdl.add_constraint(mdl.sum(lhs) >= 1) # sum el >= 1 (at least one el in sol)

    # cost function
    mdl.minimize(mdl.sum(x[s] for s in el))
    mdl.parameters.timelimit = max_solve_time
    mdl.parameters.threads = n_threads
    mdl.solve(log_output=False)
    #mdl.print_information()
    #mdl.print_solution()

    ind = sol(x)

    return ind


if __name__ == '__main__':
    
    H = [[1,2,5],[2,3,4],[1,3],[6]]
    ind = hitting_sets_problem(H)
    print(ind)