

"""
In this script there are all the functions that will create the matrices and vectors
for our ILP formalisation
"""
import numpy as np
import os



def decision_variables(I):
    """
    This function returns a dictionary with all the keys of the decision variables
    """
    from definitions import Variable
    
    P = I.problem
    mdl = I.model
    for id,b in P.bids.items():
        var = Variable(id=id,category='x')
        var.elements = [b]
        I.variables.update({id:var})
        I.var_keys.update({b.id:id})

    keys = list(I.variables.keys())

    # defining variables
    x = mdl.binary_var_dict(keys,name='x')
    return None

def decision_variables_dict(I):
    """
    This function returns a dictionary with all the keys of the decision variables
    """
    from definitions import Variable
    
    P = I.problem
    
    for id,b in P.bids.items():
        var = Variable(id=id,category='x')
        var.elements = [b]
        I.variables.update({id:var})
        I.var_keys.update({b.id:id})

    keys = list(I.variables.keys())

    return None

def decision_variables_lp(I):
    """
    This function returns a dictionary with all the keys of the decision variables
    """
    from definitions import Variable
    
    mdl = I.model_lp
    keys = list(I.variables.keys())

    # defining variables
    x = mdl.continuous_var_dict(keys,lb=0.0, ub=1.0,name='xc')
    return None

def get_variables(model,name: str, keys:list):
    x = {}
    for i in keys:
        x.update({i:model.get_var_by_name(f'{name}_{i}')})
    return x

def goods_contraint(I):
    """
    This function builds goods constraint
    sum_{b C B} x_{b} <= 1
    """
    from definitions import Constraint

    P = I.problem
    n = P.n_goods + P.n_dummies
    mdl = I.model
    var = I.variables
    keys = list(var.keys())
    x = get_variables(mdl,'x',keys)

    index = len(list(I.constraints.keys()))
    for g in range(n):
        con = Constraint(id=index,category='goods')
        con.elements.update({'good':g})
        sum_list = []
        for id,b in P.bids.items():
            if g in b.goods:
                h = I.var_keys[b.id]
                con.scope.update({h:b})
                sum_list += [x[h]]
        
        mdl.add_constraint(mdl.sum(sum_list) <= 1)
        I.constraints.update({index:con})
        I.con_keys.update({('goods',g):index})
        index += 1

    return None

def constraint_generation(I):
    """
    This function returns a dictionary with all the constraints
    """
    goods_contraint(I)
    
    return None

def objective_generation(I):
    """
    This function creates the objective function
    """
    from definitions import Objective
    P = I.problem
    mdl = I.model
    var = I.variables
    keys = list(var.keys())
    x = get_variables(mdl,'x',keys)
    
    sum_list = []
    ob = Objective(id=1)
    for id,b in P.bids.items():
        j = I.var_keys[b.id]
        ob.scope.update({j:b.id})
        sum_list += [b.prize*x[j]]

    mdl.maximize(mdl.sum(sum_list))

    return None

def goods_contraint_lp(I):
    """
    This function builds goods constraint
    sum_{b C B} x_{b} <= 1
    """
    from definitions import Constraint

    P = I.problem
    n = P.n_goods + P.n_dummies
    mdl = I.model_lp
    var = I.variables
    keys = list(var.keys())
    x = get_variables(mdl,'xc',keys)

    for g in range(n):
        sum_list = []
        for id,b in P.bids.items():
            if g in b.goods:
                h = I.var_keys[b.id]
                sum_list += [x[h]]
        
        mdl.add_constraint(mdl.sum(sum_list) <= 1)

    return None

def constraint_generation_lp(I):
    """
    This function returns a dictionary with all the constraints
    """
    goods_contraint_lp(I)
    
    return None

def objective_generation_lp(I):
    """
    This function creates the objective function
    """
    from definitions import Objective
    P = I.problem
    mdl = I.model_lp
    var = I.variables
    keys = list(var.keys())
    x = get_variables(mdl,'xc',keys)
    
    sum_list = []
    for id,b in P.bids.items():
        j = I.var_keys[b.id]
        sum_list += [b.prize*x[j]]

    mdl.maximize(mdl.sum(sum_list))

    return None

def goods_contraint_dict_old(I):
    """
    This function builds goods constraint
    sum_{b C B} x_{b} <= 1
    """
    from definitions import Constraint

    P = I.problem
    n = P.n_goods + P.n_dummies
    n_bids = len(P.bids.keys())

    index = len(list(I.constraints.keys()))
    for g in range(n):
        con = Constraint(id=index,category='goods')

        con.elements.update({'good':g})
        array_ = np.zeros(n_bids,dtype=np.int8)
        for id,b in P.bids.items():
            if g in b.goods:
                h = I.var_keys[b.id]
                con.scope.update({h:b})
                array_[h] = 1
        
        con.lhs = array_
        con.rhs = 1
        con.rel = '<='
        I.constraints.update({index:con})
        I.con_keys.update({('goods',g):index})
        index += 1

    return None

def goods_contraint_dict(I):
    """
    This function builds goods constraint
    sum_{b C B} x_{b} <= 1
    """
    from definitions import Constraint

    P = I.problem
    n = P.n_goods + P.n_dummies
    n_bids = len(P.bids.keys())

    index = len(list(I.constraints.keys()))
    for g in range(n):
        con = Constraint(id=index,category='goods')

        con.elements.update({'good':g})
        
        for id,b in P.bids.items():
            if g in b.goods:
                h = I.var_keys[b.id]
                con.scope.update({h:b})
                con.ind += [h]
                con.lhs += [1]
        
        con.rhs = 1
        con.rel = '<='
        I.constraints.update({index:con})
        I.con_keys.update({('goods',g):index})
        index += 1

    return None

def constraint_generation_dict(I):
    """
    This function returns a dictionary with all the constraints
    """
    goods_contraint_dict(I)
    
    return None


if __name__ == '__main__':
    
    path = os.getcwd()
    folder = os.path.join(path,'data')
    file = os.path.join(folder,'j30','j3016_7.sm')
    
    from read_files import read_instance
    P = read_instance(file)

    
    counter = 0
    for a in P.activities:
        counter += a.duration
        print(f"{a}, {a.duration}")
    
    print(f"Total Duration: {counter}")

    