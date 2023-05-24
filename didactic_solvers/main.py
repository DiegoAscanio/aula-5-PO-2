from branch_and_bound import *
from ppbtree import *
import sys

problems = [
    LP(
        num_vars = 5,
        num_constraints = 4,
        constraint_coeffs = [
            [5, 7, 9, 2, 1],
            [18, 4, -9, 10, 12],
            [4, 7, 3, 8, 5],
            [5, 13, 16, 3, -7],
        ],
        bounds = [250, 285, 211, 315],
        objective_coeffs = [7, 8, 2, 9, 6]
    ),
    LP(
        num_vars = 2,
        num_constraints = 1,
        constraint_coeffs = [
            [4, 2]
        ],
        bounds = [11],
        objective_coeffs = [3, 1]
    ),
    LP(
        num_vars = 2,
        num_constraints = 2,
        constraint_coeffs = [
            [180, 100],
            [2,     4]
        ],
        bounds = [800, 20],
        objective_coeffs = [1, 1]
    ),
    LP(
        num_vars = 2,
        num_constraints = 2,
        constraint_coeffs = [
            [180, 100],
            [2,     4]
        ],
        bounds = [800, 20],
        objective_coeffs = [2, 1]
    )
]

problem = problems[0]

bb_solver = BranchAndBoundMaximizationIP(problem)
bb_solver.solve()
tree = bb_solver.root_problem

print(bb_solver.optimal_solution)
print(bb_solver.optimal_value)
with open('arvore_bb.txt', 'w') as sys.stdout:
    print_tree(tree,left_child='left',right_child='right',nameattr='relaxed_lp')
