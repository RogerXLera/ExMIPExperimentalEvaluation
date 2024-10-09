
from docplex.mp.model import Model
import numpy as np

def sol(y):

    ind = []
    for i in y.keys():
        if y[i].solution_value >= 0.9:
            ind += [i]
    return ind

def mfs_problem_implicit(I,forced_constraints:list = [],max_solve_time=60.0,n_threads=1):
    """
        This function solves the Maximum Feasible Subsystem (MFS) problem
        forced_constraints: constraints to be satisfied: y_i = 0
    """
    
    mdl = Model()
    var = I.variables
    cons = I.constraints
    keys = list(var.keys())
    keys_c = list(cons.keys())
    # defining variables
    x = mdl.binary_var_dict(keys,name='x')
    y = mdl.binary_var_dict(keys_c,name='y')

    # defining constraints
    z_counter = 0
    for c,con in cons.items():
        if c in forced_constraints:
            M = 0 # we force the constraint
        else:
            abs_array = np.abs(con.lhs)
            abs_term = np.abs(con.rhs)
            M = np.sum(abs_array + abs_term)

        if con.rel == '<=':
            mdl.add_constraint(mdl.sum(con.lhs[i]*x[i] for i in range(len(keys)))
                                  <= con.rhs + M*y[c])
        
        elif con.rel == '>=':
            mdl.add_constraint(mdl.sum(con.lhs[i]*x[i] for i in range(len(keys)))
                                  >= con.rhs - M*y[c])
            
        elif con.rel == '==':
            z = mdl.continuous_var(lb=-M*1.0,ub=M*1.0,name=f'z{z_counter}')
            z_counter += 1
            mdl.add_constraint(mdl.sum(con.lhs[i]*x[i] for i in range(len(keys)))
                                  == con.rhs + z)
            mdl.add_constraint(z <= 1.0*M*y[c])
            mdl.add_constraint(z >= (-1.0)*M*y[c])

    # cost function
    mdl.minimize(mdl.sum(y[c] for c in cons.keys()))
    mdl.parameters.timelimit = max_solve_time
    mdl.parameters.threads = n_threads
    mdl.solve(log_output=False)
    #mdl.print_information()
    #mdl.print_solution()

    ind = sol(y)

    return ind

def mfs_problem_old(I,forced_constraints:list = [],max_solve_time=60.0,n_threads=1):
    """
        This function solves the Maximum Feasible Subsystem (MFS) problem
        forced_constraints: constraints to be satisfied: y_i = 0
    """
    
    mdl = Model()
    var = I.variables
    cons = I.constraints
    keys = list(var.keys())
    keys_c = list(cons.keys())

    # defining variables
    x = mdl.binary_var_dict(keys,name='x')
    y = mdl.binary_var_dict(keys_c,name='y')

    # defining constraints
    z_counter = 0
    for c,con in cons.items():
        
        if c in forced_constraints:
            mdl.add_constraint(y[c] == 0) # we force the constraint
            
        abs_array = np.abs(con.lhs)
        abs_term = np.abs(con.rhs)
        M = np.sum(abs_array + abs_term)

        if con.rel == '<=':
            mdl.add_constraint(mdl.sum(con.lhs[i]*x[i] for i in range(len(keys)))
                                  <= con.rhs + M*y[c])
        
        elif con.rel == '>=':
            mdl.add_constraint(mdl.sum(con.lhs[i]*x[i] for i in range(len(keys)))
                                  >= con.rhs - M*y[c])
            
        elif con.rel == '==':
            z = mdl.continuous_var(lb=-M*1.0,ub=M*1.0,name=f'z{z_counter}')
            z_counter += 1
            mdl.add_constraint(mdl.sum(con.lhs[i]*x[i] for i in range(len(keys)))
                                  == con.rhs + z)
            mdl.add_constraint(z <= 1.0*M*y[c])
            mdl.add_constraint(z >= (-1.0)*M*y[c])

    # cost function
    mdl.minimize(mdl.sum(y[c] for c in cons.keys()))
    mdl.parameters.timelimit = max_solve_time
    mdl.solve(log_output=True)
    #mdl.print_information()
    #mdl.print_solution()

    ind = sol(y)

    return ind


def mfs_problem(I,forced_constraints:list = [],max_solve_time=60.0,n_threads=1):
    """
        This function solves the Maximum Feasible Subsystem (MFS) problem
        forced_constraints: constraints to be satisfied: y_i = 0
    """
    
    mdl = Model()
    var = I.variables
    cons = I.constraints
    keys = list(var.keys())
    keys_c = list(cons.keys())

    # defining variables
    x = mdl.binary_var_dict(keys,name='x')
    y = mdl.binary_var_dict(keys_c,name='y')

    # defining constraints
    z_counter = 0
    for c,con in cons.items():
        
        if c in forced_constraints:
            mdl.add_constraint(y[c] == 0) # we force the constraint
            
        abs_array = np.abs(con.lhs)
        abs_term = np.abs(con.rhs)
        M = np.sum(abs_array + abs_term)

        if con.rel == '<=':
            mdl.add_constraint(mdl.sum(con.lhs[i]*x[con.ind[i]] for i in range(len(con.lhs)))
                                  <= con.rhs + M*y[c])
        
        elif con.rel == '>=':
            mdl.add_constraint(mdl.sum(con.lhs[i]*x[con.ind[i]] for i in range(len(con.lhs)))
                                  >= con.rhs - M*y[c])
            
        elif con.rel == '==':
            z = mdl.continuous_var(lb=-M*1.0,ub=M*1.0,name=f'z{z_counter}')
            z_counter += 1
            mdl.add_constraint(mdl.sum(con.lhs[i]*x[con.ind[i]] for i in range(len(con.lhs)))
                                  == con.rhs + z)
            mdl.add_constraint(z <= 1.0*M*y[c])
            mdl.add_constraint(z >= (-1.0)*M*y[c])

    # cost function
    mdl.minimize(mdl.sum(y[c] for c in cons.keys()))
    mdl.parameters.timelimit = max_solve_time
    mdl.solve(log_output=False)
    #mdl.print_information()
    #mdl.print_solution()

    ind = sol(y)

    return ind


if __name__ == '__main__':
    
    import argparse as ap
    import os
    
    parser = ap.ArgumentParser()
    parser.add_argument('-n', type=int, default=30, help='n: Number of activities')
    parser.add_argument('-s', type=int, default=60, help='s: Time limit in seconds')
    parser.add_argument('-q', type=int, default=1, help='q: Query type')
    parser.add_argument('-e', type=float, default=0.0, help='e: Optimality epsylon')
    parser.add_argument('-f', type=str, default = 'j301_1.sm', help='filename of the instance')
    parser.add_argument('--conflict', type=int, default=0, help='conflict: conflict algorithm')
    parser.add_argument('--seed', type=int, default=0, help='seed')
    args = parser.parse_args()
    
    path = os.getcwd()
    folder = os.path.join(path,'data')
    sub_folder = os.path.join(folder,f"j{args.n}")
    file = os.path.join(sub_folder,f"{args.f}")
    
    from read_files import read_instance
    P = read_instance(file)

    from definitions import Instance,IIS,Query
    instance_id = f"{args.f}".split('.')[0]
    I = Instance(id=instance_id,project=P)
    I.build_constraints()
    folder = os.path.join(path,'solutions')
    sub_folder = os.path.join(folder,f"j{args.n}")
    file = os.path.join(sub_folder,f"{args.f}.stdout")
    I.read_solution(file)
    from generate_query import query_generation
    import random
    random.seed(args.seed)
    q = Query(id=args.q,category=args.q)
    q_folder = os.path.join(path,'queries',f"j{args.n}")
    q_filename = os.path.join(q_folder,f"q-{args.f}-{args.q}.stdout")
    q.read(I,q_filename)
    q.query_transcription(I)
    iis = IIS(id=instance_id,instance=I,query=q)
    ind = iis.mfs([])
    print(ind)

    
