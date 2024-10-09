# -*- coding: utf-8 -*-
"""
Author: Roger X. Lera Leri
Date: 30/09/2023
"""

import cplex as cp
import numpy as np
import argparse as ap
import time
import csv
import os
from docplex.mp.model import Model


if __name__ == '__main__':
    
    parser = ap.ArgumentParser()
    parser.add_argument('-g', type=int, default=12, help='g: Number of goods')
    parser.add_argument('-b', type=int, default=20, help='b: Number of bids')
    parser.add_argument('-s', type=int, default=60, help='s: Time limit in seconds')
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
    I.solve(solution_time=args.s)
    I.print_solution()
        
    
