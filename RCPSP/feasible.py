
from docplex.cp.model import CpoModel

def cp_problem_old(I,constraint_keys,time_budget=60.0,n_threads=1):
    """
        This function builds the constraint programming problem
    """
    if len(constraint_keys) == 0:
        return True
    
    mdl = CpoModel()
    var = I.variables
    cons = I.constraints
    keys = list(var.keys())
    # defining variables
    x = mdl.binary_var_dict(keys,name='x')

    for c in constraint_keys:
        
        con = cons[c]

        if con.rel == '<=':
            mdl.add_constraint(sum(con.lhs[i]*x[i] for i in range(len(keys)))
                                  <= con.rhs )
        
        elif con.rel == '>=':
            mdl.add_constraint(sum(con.lhs[i]*x[i] for i in range(len(keys)))
                                  >= con.rhs )
            
        elif con.rel == '==':
            mdl.add_constraint(sum(con.lhs[i]*x[i] for i in range(len(keys)))
                                  == con.rhs )

    # solve model
    mdl.export_as_cpo(f'cp.cpo')
    #mdl.parameters.TimeLimit = time_budget
    #solved = mdl.solve(LogVerbosity='Quiet')
    solved = mdl.solve()
    if solved:
        return True
    else:
        return False
    
def cp_problem(I,constraint_keys,time_budget=60.0,n_threads=1):
    """
        This function builds the constraint programming problem
    """
    if len(constraint_keys) == 0:
        return True
    
    mdl = CpoModel()
    var = I.variables
    cons = I.constraints
    keys = list(var.keys())
    # defining variables
    x = mdl.binary_var_dict(keys,name='x')

    for c in constraint_keys:

        con = cons[c]

        if con.rel == '<=':
            mdl.add_constraint(sum(con.lhs[i]*x[con.ind[i]] for i in range(len(con.lhs)))
                                  <= con.rhs )
        
        elif con.rel == '>=':
            mdl.add_constraint(sum(con.lhs[i]*x[con.ind[i]] for i in range(len(con.lhs)))
                                  >= con.rhs )
            
        elif con.rel == '==':
            mdl.add_constraint(sum(con.lhs[i]*x[con.ind[i]] for i in range(len(con.lhs)))
                                  == con.rhs )

    # solve model
    #mdl.export_as_cpo(f'cp.cpo')
    #mdl.parameters.TimeLimit = time_budget
    solved = mdl.solve(LogVerbosity='Quiet')
    #solved = mdl.solve()
    if solved:
        return True
    else:
        return False


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
    status = iis.query_feasibility()
    print(f"Status: {status}")
