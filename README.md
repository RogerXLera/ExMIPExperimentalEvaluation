ExMIP: Experimental Evaluation
===================
This repository contains the implementation of the algorithms and data of the experimental section of the paper
"Exploiting Constraint Reasoning to Build Graphical Explanations for Mixed-Integer Programming" by ANONYMOUS
in the 24th International Conference on Autonomous Agents and Multiagent Systems (AAMAS), Detroit, Michigan, USA, May 19 – 23, 2025.

Dependencies
----------
 - [Python 3.10](https://www.python.org/downloads/)
 - [Numpy](https://numpy.org/)
 - [Docplex](https://www.cvxpy.org/)
 - [CPLEX](https://www.ibm.com/es-es/products/ilog-cplex-optimization-studio)


Dataset
----------

 - **RCPSP**: The single-mode RCPSP instances used come from [PSPLIB](https://www.om-db.wi.tum.de/psplib/) library.
 - **WDP**: The CA instances are generated using [CATS](https://github.com/kevinlb1/CATS) library.

Execution
----------
Our approach must be executed by means of the [`iis.py`](iis.py) Python script to use the CPLEX built-in algorithm, or [`small_iis.py`](small_iis.py) Python script to compute the smallest IIS,  i.e.,
```
usage: iis.py [-s S] [-q Q] [--file file] [specific problem arguments]

optional arguments:
  -h, --help  show this help message and exit
  -s S        time limit (default: 60)
  -q Q        query type (default: 1)
  --file FILE instance file
  
```

Acknowledgements
----------
This repository contains an adapted implemmentation of the [FORQES](https://alexeyignatiev.github.io/assets/pdf/iplms-cp15-preprint.pdf) algorithm to extract the smallest IIS. 