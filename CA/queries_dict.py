"""
Author: Roger X. Lera Leri
Date: 2024/07/10
"""
import numpy as np

def query_1(q,I):
    """
    Why is bid b selected?
    """
    from definitions import Constraint
    from formalisation import get_variables
    q_type = q.category
    P = I.problem
    n_bids = len(P.bids.keys())
    var_keys = I.var_keys
    index = len(list(I.constraints.keys()))

    b = q.elements[0][0]
    i = var_keys[b.id]
    con = Constraint(id=index,category='query')
    con.elements.update({'bid':b,'query':q_type})
    con.scope.update({i:b})
    q.scope.update({i:b})

    con.ind += [i]
    con.lhs += [1]
    con.rhs = 0
    con.rel = '=='

    I.constraints.update({index:con})
    I.con_keys.update({('query',b.id,q_type):index})

    return None

def query_2(q,I):
    """
    Why is bid b not selected?
    """
    from definitions import Constraint
    from formalisation import get_variables
    q_type = q.category
    var_keys = I.var_keys

    index = len(list(I.constraints.keys()))
    P = I.problem
    n_bids = len(P.bids.keys())

    b = q.elements[0][0]
    i = var_keys[b.id]
    con = Constraint(id=index,category='query')
    con.elements.update({'bid':b,'query':q_type})
    con.scope.update({i:b})
    q.scope.update({i:b})

    con.ind += [i]
    con.lhs += [1]
    con.rhs = 1
    con.rel = '=='
    
    I.constraints.update({index:con})
    I.con_keys.update({('query',b.id,q_type):index})

    return None

def query_3(q,I):
    """
    Why is bid b selected instead of bid b'?
    """
    from definitions import Constraint
    from formalisation import get_variables
    q_type = q.category
    var_keys = I.var_keys

    index = len(list(I.constraints.keys()))
    P = I.problem
    n_bids = len(P.bids.keys())

    b = q.elements[0][0]
    i = var_keys[b.id]
    con = Constraint(id=index,category='query')
    con.elements.update({'bid':b,'query':q_type})
    con.scope.update({i:b})
    q.scope.update({i:b})
    
    con.ind += [i]
    con.lhs += [1]
    con.rhs = 0
    con.rel = '=='

    I.constraints.update({index:con})
    I.con_keys.update({('query',b.id,q_type):index})

    b_ = q.elements[1][0]
    i_ = var_keys[b_.id]
    con_ = Constraint(id=index+1,category='query')
    con_.elements.update({'bid':b_,'query':q_type})
    con_.scope.update({i_:b_})
    q.scope.update({i_:b_})

    con_.ind += [i_]
    con_.lhs += [1]
    con_.rhs = 1
    con_.rel = '=='
    
    I.constraints.update({index+1:con_})
    I.con_keys.update({('query',b.id,b_.id,q_type):index+1})


    return None

def query_4(q,I):
    """
    Why is the subset of bids B selected?
    """
    from definitions import Constraint
    from formalisation import get_variables
    q_type = q.category
    var_keys = I.var_keys
    index = len(list(I.constraints.keys()))
    P = I.problem
    n_bids = len(P.bids.keys())


    B = [elem[0] for elem in q.elements]
    bids = [elem[0].id for elem in q.elements]
    con = Constraint(id=index,category='query')
    con.elements.update({'bids':B,'query':q_type})
    
    for b in B:
        i = var_keys[b.id]
        con.scope.update({i:b})
        q.scope.update({i:b})
        con.ind += [i]
        con.lhs += [1]

    con.rhs = 0
    con.rel = '=='
    I.constraints.update({index:con})
    I.con_keys.update({('query',q_type):index})

    return None

def query_5(q,I):
    """
    Why is the subset of bids B not selected?
    """
    from definitions import Constraint
    from formalisation import get_variables
    q_type = q.category
    var_keys = I.var_keys
    index = len(list(I.constraints.keys()))
    P = I.problem
    n_bids = len(P.bids.keys())

    B = [elem[0] for elem in q.elements]
    bids = [elem[0].id for elem in q.elements]
    con = Constraint(id=index,category='query')
    con.elements.update({'bids':B,'query':q_type})
    
    for b in B:
        i = var_keys[b.id]
        con.scope.update({i:b})
        q.scope.update({i:b})
        con.ind += [i]
        con.lhs += [1]

    sum_ = sum(con.lhs)
    con.rhs = sum_
    con.rel = '=='
    I.constraints.update({index:con})
    I.con_keys.update({('query',q_type):index})

    return None

def query_6(q,I):
    """
    Why is the subset of bids B selected, instead of B'?
    """
    from definitions import Constraint
    from formalisation import get_variables
    q_type = q.category
    var_keys = I.var_keys
    index = len(list(I.constraints.keys()))
    P = I.problem
    n_bids = len(P.bids.keys())

    B_T = [elem[0] for elem in q.elements]
    len_b = len(B_T)
    len_b_2 = int(len_b/2)
    B = B_T[:len_b_2]
    B_ = B_T[len_b_2:]
    bids = [b.id for b in B]
    bids_ = [b_.id for b_ in B_]

    con = Constraint(id=index,category='query')
    con.elements.update({'bids':B,'query':q_type})
    for b in B:
        i = var_keys[b.id]
        con.scope.update({i:b})
        q.scope.update({i:b})
        con.ind += [i]
        con.lhs += [1]

    con.rhs = 0
    con.rel = '=='
    I.constraints.update({index:con})
    I.con_keys.update({('query',q_type):index})

    con_ = Constraint(id=index+1,category='query')
    con_.elements.update({'bids':B_,'query':q_type})
    for b_ in B_:
        i = var_keys[b_.id]
        con_.scope.update({i:b_})
        q.scope.update({i:b_})
        con_.ind += [i]
        con_.lhs += [1]

    sum_ = sum(con_.lhs)
    con_.rhs = sum_
    con_.rel = '=='
    I.constraints.update({index+1:con_})
    I.con_keys.update({('query',q_type):index+1})

    return None

def query_7(q,I):
    """
    Why is good g selected?
    """
    from definitions import Constraint
    from formalisation import get_variables
    q_type = q.category
    B_dic = I.problem.bids
    var_keys = I.var_keys
    index = len(list(I.constraints.keys()))
    n_bids = len(B_dic.keys())

    g = q.elements[0][0]
    B = [b for id_,b in B_dic.items() if g in b.goods]
    bids = [b.id for b in B]
    con = Constraint(id=index,category='query')
    con.elements.update({'good':g,'query':q_type})
    
    for b in B:
        i = var_keys[b.id]
        con.scope.update({i:b})
        q.scope.update({i:b})
        con.ind += [i]
        con.lhs += [1]

    con.rhs = 0
    con.rel = '=='
    I.constraints.update({index:con})
    I.con_keys.update({('query',g,q_type):index})

    return None

def query_8(q,I):
    """
    Why is good g not selected?
    """
    from definitions import Constraint
    from formalisation import get_variables
    q_type = q.category
    B_dic = I.problem.bids
    var_keys = I.var_keys
    index = len(list(I.constraints.keys()))
    n_bids = len(B_dic.keys())

    g = q.elements[0][0]
    B = [b for id_,b in B_dic.items() if g in b.goods]
    bids = [b.id for b in B]
    con = Constraint(id=index,category='query')
    con.elements.update({'good':g,'query':q_type})
    
    for b in B:
        i = var_keys[b.id]
        con.scope.update({i:b})
        q.scope.update({i:b})
        con.ind += [i]
        con.lhs += [1]

    con.rhs = 1
    con.rel = '=='
    I.constraints.update({index:con})
    I.con_keys.update({('query',g,q_type):index})

    return None

def query_9(q,I):
    """
    Why is good g selected instead of good g'?
    """
    from definitions import Constraint
    from formalisation import get_variables
    q_type = q.category
    B_dic = I.problem.bids
    var_keys = I.var_keys
    index = len(list(I.constraints.keys()))
    n_bids = len(B_dic.keys())
    g = q.elements[0][0]
    B = [b for id_,b in B_dic.items() if g in b.goods]
    bids = [b.id for b in B]
    con = Constraint(id=index,category='query')
    con.elements.update({'good':g,'query':q_type})
    
    array_ = np.zeros(n_bids,dtype=np.int8)
    for b in B:
        i = var_keys[b.id]
        con.scope.update({i:b})
        q.scope.update({i:b})
        con.ind += [i]
        con.lhs += [1]

    con.rhs = 0
    con.rel = '=='
    I.constraints.update({index:con})
    I.con_keys.update({('query',g,q_type):index})

    g_ = q.elements[1][0]
    B = [b for id_,b in B_dic.items() if g_ in b.goods]
    bids = [b.id for b in B]
    
    con = Constraint(id=index+1,category='query')
    con.elements.update({'good':g_,'query':q_type})
    
    for b in B:
        i = var_keys[b.id]
        con.scope.update({i:b})
        q.scope.update({i:b})
        con.ind += [i]
        con.lhs += [1]

    con.rhs = 1
    con.rel = '=='
    I.constraints.update({index+1:con})
    I.con_keys.update({('query',g_,q_type):index+1})

    return None

def query_10(q,I):
    """
    Why are goods g and g' in the same bid?
    """
    from definitions import Constraint
    from formalisation import get_variables
    q_type = q.category
    B_dic = I.problem.bids
    var_keys = I.var_keys
    n_bids = len(B_dic.keys())
    index = len(list(I.constraints.keys()))

    g = q.elements[0][0]
    g_ = q.elements[1][0]
    B = [b for id_,b in B_dic.items() if g in b.goods and g_ in b.goods]
    if len(B) == 0:
        print(f"Query {q_type} impossible to generate.")
        raise ValueError(f"No bid with goods {g} and {g_} exists.")
    bids = [b.id for b in B]
    con = Constraint(id=index,category='query')
    con.elements.update({'goods':[g,g_],'query':q_type})
    
    for b in B:
        i = var_keys[b.id]
        con.scope.update({i:b})
        q.scope.update({i:b})
        con.ind += [i]
        con.lhs += [1]

    con.rhs = 0
    con.rel = '=='
    I.constraints.update({index:con})
    I.con_keys.update({('query',g,g_,q_type):index})

    return None

def query_11(q,I):
    """
    Why are goods g and g' not in the same bid?
    """
    from definitions import Constraint
    from formalisation import get_variables
    q_type = q.category
    B_dic = I.problem.bids
    var_keys = I.var_keys
    n_bids = len(B_dic.keys())
    index = len(list(I.constraints.keys()))

    g = q.elements[0][0]
    g_ = q.elements[1][0]
    B = [b for id_,b in B_dic.items() if g in b.goods and g_ in b.goods]
    if len(B) == 0:
        print(f"Query {q_type} impossible to generate.")
        raise ValueError(f"No bid with goods {g} and {g_} exists.")
    bids = [b.id for b in B]
    con = Constraint(id=index,category='query')
    con.elements.update({'goods':[g,g_],'query':q_type})
    
    for b in B:
        i = var_keys[b.id]
        con.scope.update({i:b})
        q.scope.update({i:b})
        con.ind += [i]
        con.lhs += [1]

    con.rhs = 1
    con.rel = '=='
    I.constraints.update({index:con})
    I.con_keys.update({('query',g,g_,q_type):index})

    return None



def query_transcription_(q,I):
    """
    This function encodes the queries into the model
    """
    function = globals().get(f"query_{q.category}")
    function(q,I)


if __name__ == '__main__':
    
    import argparse as ap
    import os
    print('Query translation')
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
    from generate_query import query_generation
    Q = query_generation(I,args.q)
    for q in Q:
        q.query_transcription(I)
        for key,item in q.scope.items():
            print(item.id)