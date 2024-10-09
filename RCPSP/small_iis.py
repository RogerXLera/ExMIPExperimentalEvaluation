
import numpy as np

def maximality_constraint(IIS,e:float = 0.0):
    """
        This function builds the maximality constraint
    """
    from definitions import Constraint
    from formalisation import get_variables
    I = IIS.instance
    P = I.project
    a_J = P.activities[-1]
    f_value = I.objective_value + e
    var = I.variables
    N = len(var)

    index = len(list(I.constraints.keys()))

    array_ = np.zeros(N)
    con = Constraint(id=index,category='max')
    con.elements.update({'f':f_value,'objective':'max'})
    for t in range(a_J.ef_time,a_J.lf_time+1):
        j = I.var_keys[(a_J.id,t)]
        con.scope.update({j:(a_J,t)})
        con.ind += [j]
        con.lhs += [t]


    # we add the maximality constraint
    # since we aim to minimise, sum has to be lower than f^*
    con.rhs = f_value
    con.rel = '<='
    I.constraints.update({index:con})
    I.con_keys.update({('max',f_value):index})
    return None

def smallest_IIS(IIS,time_lim = 60.0,n_threads=1):
    
    from feasible import cp_problem
    from mfs import mfs_problem
    from hitting_sets import hitting_sets_problem
    import time

    I = IIS.instance
    var = I.variables
    keys = list(var.keys())
    cons = I.constraints
    st = time.time()
    H = []
    i = 0
    while time.time() - st <= time_lim:
        h = hitting_sets_problem(H, time_lim - (time.time() - st),n_threads)
        F_ = h
        if time_lim - (time.time() - st) < 0:
            break
        cp_stat = cp_problem(I,F_,time_lim - (time.time() - st),n_threads)
        if cp_stat: # if feasible, grow
            #print(F_)
            if time_lim - (time.time() - st) < 0:
                break
            C = mfs_problem(I,F_,time_lim - (time.time() - st),n_threads)
        else: # if infeasible, SMUS
            print(f"Optimal IIS")
            break

        if len(C) == 0:
            break
        else:
            H += [C]

        i += 1
        print(f"Iter {i}: ")
        print(f"Min Hitting Set: {F_}")
        print(f"Min Correction Subset: {C}")

    run_time = time.time() - st
    IIS.solution_time = run_time

    for c in F_:
        IIS.constraints.update({c:cons[c]})

    return None


def read_iis(IIS,filename):
    """
        This function reads the IIS
    """
    num_str = [str(i) for i in range(10)]
    q = IIS.query
    I = IIS.instance
    A = I.project.activities
    
    with open(filename,'r') as f:
        lines = f.readlines()
    if len(lines) == 0:
        IIS.computed = False
        IIS.optimality = 'time'
        return None
    first_line = lines[0]
    if "IIS generation" in first_line:
        IIS.computed = True
    elif "query" in first_line or "Query" in first_line:
        IIS.computed = False
        IIS.optimality = 'query'
        return None
    else:
        IIS.computed = False
        IIS.optimality = 'time'
        return None

    for l in lines[1:]:
        info_type = l.split(':')[0]
        array_ = l.split(':')[1:]
        if info_type == 'Query element':
            list_ = array_[0].split(',')
            if q.category == 11:
                q.elements += [[list_[0],int(list_[1]),int(list_[2])]]
            else:
                a = A[int(list_[0])-1]
                q.elements += [[a,int(list_[1])]]

        elif info_type == 'IIS optimality':
            index_ = array_[0].strip()
            IIS.optimality = index_
        elif info_type == 'IIS solution time':
            index_ = array_[0].strip()
            IIS.solution_time = float(index_)
        elif info_type == 'IIS Constraint':
            index_ = array_[0].strip().split(';')[0]
            IIS.constraints.update({int(index_):None})

    return None



if __name__ == '__main__':
    
    import argparse as ap
    import os
    print("IIS generation")    
    parser = ap.ArgumentParser()
    parser.add_argument('-n', type=int, default=30, help='n: Number of activities')
    parser.add_argument('-s', type=int, default=60, help='s: Time limit in seconds')
    parser.add_argument('-q', type=int, default=1, help='q: Query type')
    parser.add_argument('-t', type=int, default=1, help='t: number of threads')
    parser.add_argument('-e', type=float, default=0.0, help='e: Optimality epsylon')
    parser.add_argument('-f', type=str, default = 'j301_1.sm', help='filename of the instance')
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
    q = Query(id=args.q,category=args.q)
    q_folder = os.path.join(path,'queries',f"j{args.n}")
    q_filename = os.path.join(q_folder,f"q-{args.f}-{args.q}.stdout")
    q.read(I,q_filename)
    q.query_transcription(I)
    iis = IIS(id=instance_id,instance=I,query=q)
    iis.compute(args.e,args.s,n_threads=args.t,small=True)
    iis.print_iis()
        
