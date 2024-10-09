
import json
import os
import numpy as np

def line_mode(line:str):
    
    if len(line) > 0:
        return line[0]
    else:
        return None

def read_bid(P, line:str):
    from definitions import Bid

    tokens = line.split('\t')
    b = Bid(id=int(tokens[0]))
    b.prize = float(tokens[1])
    b.goods += [int(tokens[i]) for i in range(2,len(tokens)-1)]
    P.bids.update({b.id:b})
    return None

def read_line(P,line:str):
    
    line = line.split('\n')[0]
    mode = line_mode(line)
    tokens = line.split(' ')
    num_str = [f'{i}' for i in range(10)]
    
    if mode == 'g':
        P.n_goods = int(tokens[1])
        return None
    elif mode == 'd':
        P.n_dummies = int(tokens[1])
        return None
    elif mode in num_str:
        read_bid(P, line)
        return None
    else:
        return None


def read_instance(filepath):
    """
    This function reads a generic file containing the info of the instance
    and it stores it in objects. 
    """
    from definitions import Problem
    
    P = Problem(id=1)
    with open(filepath,'r') as inputfile:
        data = inputfile.readlines()
        for line in data:
            read_line(P,line)

    return P


def read_solution_file(file_path):
    
    solution = {}
    f = 0.0
    t = 0.0
    with open(file_path, 'r') as f:
        data = f.readlines()
        for row in data:
            if "Bid" in row: #process activities
                bid = row.split("Bid: ")[1]
                bid_id = bid.split(" ")[0]
                solution.update({int(bid_id):[int(bid_id)]})
            elif "Objective" in row:
                objective = row.split("Objective value: ")[1]
                f = float(objective.split(" ")[0])
            elif "Solving" in row:
                time_ = row.split("Solving time: ")[1]
                t = float(time_.split(" ")[0])

    return solution,f,t


if __name__ == '__main__':
    
    path = os.getcwd()
    folder = os.path.join(path,'data')
    file = os.path.join(folder,'12-20','paths-12-20-10000.txt')
    P = read_instance(file)
    for id_,b in P.bids.items():
        print(f"{b}, {b.prize:.3f}, {b.goods}")

    
    
    
    
    
    
    
    
    

    