
import random as rd

def generate_query_1(I,Q,n_q=1):
    """
    Why is bid b selected?
    """
    from definitions import Query
    solution = I.solution_values
    variables = I.variables
    len_q = len(Q)
    solutions_c = list(solution.keys()).copy()
    for i in range(n_q):
        len_ = len(solutions_c)
        n = rd.randint(0,len_-1)
        var = variables[solutions_c[n]]
        q = Query(id=len_q + i,category=1)
        q.elements = [var.elements]
        Q += [q]
        solutions_c.pop(n)
    return None

def generate_query_2(I,Q,n_q=1):
    """
    Why is bid b not selected?
    """
    from definitions import Query
    solution = I.solution_values
    variables = I.variables
    not_selected_keys = [k for k in variables.keys() if k not in solution.keys()]
    len_q = len(Q)
    for i in range(n_q):
        len_ = len(not_selected_keys)
        n = rd.randint(0,len_-1)
        var = variables[not_selected_keys[n]]
        q = Query(id=len_q + i,category=2)
        q.elements = [var.elements]
        Q += [q]
        not_selected_keys.pop(n)
    return None

def generate_query_3(I,Q,n_q=1):
    """
    Why is bid b selected instead of bid b'?
    """
    from definitions import Query
    solution = I.solution_values
    variables = I.variables
    not_selected_keys = [k for k in variables.keys() if k not in solution.keys()]
    len_q = len(Q)
    solutions_c = list(solution.keys()).copy()
    for i in range(n_q):
        len_ = len(solutions_c)
        len_p = len(not_selected_keys)
        n = rd.randint(0,len_-1)
        n_p = rd.randint(0,len_p-1)
        var = variables[solutions_c[n]]
        var_p = variables[not_selected_keys[n_p]]
        q = Query(id=len_q + i,category=3)
        q.elements = [var.elements,var_p.elements]
        Q += [q]
        solutions_c.pop(n)
        not_selected_keys.pop(n_p)
    return None

def generate_query_4(I,Q,n_q=1):
    """
    Why is the subset of bids B selected?
    """
    from definitions import Query
    solution = I.solution_values
    variables = I.variables
    len_q = len(Q)
    for i in range(n_q):
        solutions_c = list(solution.keys()).copy()
        len_ = len(solutions_c)
        n_bids = rd.randint(2,len_)
        q = Query(id=len_q + i,category=4)
        for j in range(n_bids):
            n = rd.randint(0,len(solutions_c)-1)
            var = variables[solutions_c[n]]
            q.elements += [var.elements]
            solutions_c.pop(n)
        Q += [q]
    return None

def generate_query_5(I,Q,n_q=1):
    """
    Why is the subset of bids B not selected?
    """
    from definitions import Query
    solution = I.solution_values
    variables = I.variables
    len_q = len(Q)
    not_selected_keys_o = [k for k in variables.keys() if k not in solution.keys()]
    for i in range(n_q):
        not_selected_keys = not_selected_keys_o.copy()
        len_ = len(not_selected_keys)
        n_bids = rd.randint(2,len_)
        q = Query(id=len_q + i,category=5)
        for j in range(n_bids):
            n = rd.randint(0,len(not_selected_keys)-1)
            var = variables[not_selected_keys[n]]
            q.elements += [var.elements]
            not_selected_keys.pop(n)
        Q += [q]
    return None

def generate_query_6(I,Q,n_q=1):
    """
    Why is the subset of bids B selected instead of B'?
    """
    from definitions import Query
    solution = I.solution_values
    variables = I.variables
    len_q = len(Q)
    not_selected_keys_o = [k for k in variables.keys() if k not in solution.keys()]
    for i in range(n_q):
        solutions_c = list(solution.keys()).copy()
        not_selected_keys = not_selected_keys_o.copy()
        len_ = len(solutions_c)
        len_p = len(not_selected_keys)
        len_min = min(len_,len_p)
        n_bids = rd.randint(2,len_min)
        q = Query(id=len_q + i,category=6)
        for j in range(n_bids):
            n = rd.randint(0,len(solutions_c)-1)
            n_p = rd.randint(0,len(not_selected_keys)-1)
            var = variables[solutions_c[n]]
            var_p = variables[not_selected_keys[n_p]]
            q.elements.insert(0,var.elements)
            q.elements.append(var_p.elements)
            solutions_c.pop(n)
            not_selected_keys.pop(n_p)
        Q += [q]
    return None

def generate_query_7(I,Q,n_q=1):
    """
    Why is good g selected?
    """
    from definitions import Query
    solution = I.solution_values
    problem = I.problem
    bids = problem.bids
    selected_goods = [g for k in solution.keys() for g in bids[k].goods]
    len_q = len(Q)
    for i in range(n_q):
        len_ = len(selected_goods)
        n = rd.randint(0,len_-1)
        good = selected_goods[n]
        q = Query(id=len_q + i,category=7)
        q.elements = [[good]]
        Q += [q]
        selected_goods.pop(n)
    return None

def generate_query_8(I,Q,n_q=1):
    """
    Why is good g not selected?
    """
    from definitions import Query
    solution = I.solution_values
    problem = I.problem
    bids = problem.bids
    selected_goods = [g for k in solution.keys() for g in bids[k].goods]
    not_selected_goods = [k for k in range(problem.n_goods) if k not in selected_goods]
    len_q = len(Q)
    for i in range(n_q):
        len_ = len(not_selected_goods)
        n = rd.randint(0,len_-1)
        good = not_selected_goods[n]
        q = Query(id=len_q + i,category=8)
        q.elements = [[good]]
        Q += [q]
        not_selected_goods.pop(n)
    return None

def generate_query_9(I,Q,n_q=1):
    """
    Why is good g selected instead of g'?
    """
    from definitions import Query
    solution = I.solution_values
    problem = I.problem
    bids = problem.bids
    selected_goods = [g for k in solution.keys() for g in bids[k].goods]
    not_selected_goods = [k for k in range(problem.n_goods) if k not in selected_goods]
    len_q = len(Q)
    for i in range(n_q):
        len_ = len(selected_goods)
        n = rd.randint(0,len_-1)
        good = selected_goods[n]
        len_p = len(not_selected_goods)
        n_p = rd.randint(0,len_p-1)
        good_p = not_selected_goods[n_p]
        q = Query(id=len_q + i,category=9)
        q.elements = [[good],[good_p]]
        Q += [q]
        not_selected_goods.pop(n_p)
        selected_goods.pop(n)
    return None

def generate_query_10(I,Q,n_q=1):
    """
    Why are good g and g' in the same bid?
    """
    from definitions import Query
    solution = I.solution_values
    problem = I.problem
    bids = problem.bids
    selected_bids = [b for b in solution.keys() if len(bids[b].goods) >= 2]
    len_q = len(Q)
    for i in range(n_q):
        len_ = len(selected_bids)
        n = rd.randint(0,len_-1)
        bid = selected_bids[n]
        selected_bids.pop(n)
        selected_goods = bids[bid].goods.copy()
        len_b = len(selected_goods)
        ng1 = rd.randint(0,len_b-1)
        good1 = selected_goods[ng1]
        selected_goods.pop(ng1)
        ng2 = rd.randint(0,len_b-2)
        good2 = selected_goods[ng2]
        q = Query(id=len_q + i,category=10)
        q.elements = [[good1],[good2]]
        Q += [q]
    return None


def generate_query_11(I,Q,n_q=1):
    """
    Why are good g and g' not in the same bid?
    """
    from definitions import Query
    solution = I.solution_values
    problem = I.problem
    bids = problem.bids
    len_bids = len(bids.keys())
    selected_bids = [b for b in solution.keys()]
    len_q = len(Q)
    for i in range(n_q):
        len_ = len(selected_bids)
        n = rd.randint(0,len_-1)
        bid = selected_bids[n]
        len_bid = len(bids[bid].goods)
        ng1 = rd.randint(0,len_bid-1)
        good1 = bids[bid].goods[ng1]
        selected_bids.pop(n)
        bids_p = [b for id_,b in bids.items() if good1 in b.goods and len(b.goods) > 1]
        np = rd.randint(0,len(bids_p)-1)
        bidp = bids_p[np]
        bidp_goods = bidp.goods.copy()
        bidp_goods.remove(good1)
        len_bidp = len(bidp_goods)
        ng2 = rd.randint(0,len_bidp-1)
        good2 = bidp_goods[ng2]
        q = Query(id=len_q + i,category=11)
        q.elements = [[good1],[good2]]
        Q += [q]
    return None


def query_generation(I,category: int = 1, n_q: int = 1):
    """
    This function encodes the queries into the model
    """

    function = globals().get(f"generate_query_{category}")
    Q = []
    function(I,Q,n_q)
    return Q


if __name__ == '__main__':
    
    import argparse as ap
    import os
    print('Query generation')
    parser = ap.ArgumentParser()
    parser.add_argument('-g', type=int, default=12, help='g: Number of goods')
    parser.add_argument('-b', type=int, default=20, help='b: Number of bids')
    parser.add_argument('-s', type=int, default=60, help='s: Time limit in seconds')
    parser.add_argument('-q', type=int, default=1, help='q: Query type')
    parser.add_argument('-f', type=str, default = 'paths-12-20-10000.txt', help='filename of the instance')
    args = parser.parse_args()
    
    path = os.getcwd()
    folder = os.path.join(path,'data')
    sub_folder = os.path.join(folder,f"{args.g}-{args.b}")
    file = os.path.join(sub_folder,f"{args.f}")
    
    from read_files import read_instance
    P = read_instance(file)

    from definitions import Instance
    I = Instance(id=0,problem=P)
    I.build_model()
    folder = os.path.join(path,'solutions')
    sub_folder = os.path.join(folder,f"{args.g}-{args.b}")
    file = os.path.join(sub_folder,f"{args.f}.stdout")
    I.read_solution(file)
    Q = query_generation(I,11)
    for q in Q:
        print("Type: ",q.category)
        for i in range(len(q.elements)):
            print(q.elements[i][0])
    