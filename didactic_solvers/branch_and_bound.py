import numpy as np
import random
import pdb
from copy import deepcopy as copy
from datetime import datetime, timedelta
from ortools.linear_solver import pywraplp

new_solver = pywraplp.Solver.CreateSolver
infinity = np.inf
TIME_LIMIT=180

# funcoes auxiliares
def all_variables_are_integer(variables):
    for i in range(len(variables)):
        value = variables[i].solution_value()
        if np.round(value, decimals=10) % 1 != 0:
            return False
    return True

def pick_variable_and_return_its_lower_bound(variables):
    for i in range(len(variables)):
        value = variables[i].solution_value()
        if np.round(value, decimals=10) % 1 != 0:
            return i, np.floor(value)

class LP:
    def __add_leq_restrictions(self, solver, x):
        for i in range(self.num_constraints):
            if self.bounds[i] >= 0:
                constraint = solver.RowConstraint(
                    0, self.bounds[i]
                )
                for j in range(self.num_vars):
                    constraint.SetCoefficient(
                        x[j], self.constraint_coeffs[i][j]
                    )
        return solver

    def __add_geq_restrictions(self, solver, x):
        for i in range(self.num_constraints):
            if self.bounds[i] < 0:
                constraint = solver.RowConstraint(
                    -self.bounds[i], solver.infinity()
                )
                for j in range(self.num_vars):
                    if self.constraint_coeffs[i][j] < 0:
                        constraint.SetCoefficient(
                            x[j], -self.constraint_coeffs[i][j]
                        )
                    else:
                        constraint.SetCoefficient(
                            x[j], self.constraint_coeffs[i][j]
                        )
        return solver

    def __create_solver(self):
        # definindo solver
        solver = new_solver('GLOP')
        # adicionando variaveis
        x = {}
        for i in range(self.num_vars):
            x[i] = solver.NumVar(0, solver.infinity(), 'x_{}'.format(i))
        # adicionando restricoes menor ou igual
        solver = self.__add_leq_restrictions(solver, x)
        # adicionando restricoes maior ou igual
        solver = self.__add_geq_restrictions(solver, x)

        # definindo o objetivo
        objective = solver.Objective()
        for i in range(self.num_vars):
            objective.SetCoefficient(
                x[i], self.objective_coeffs[i]
            )
        objective.SetMaximization()
        # retornando o solver e suas variaveis
        return solver

    @property
    def future_solver(self):
        return self.__create_solver()

    def __str__(self):
        if self.status != pywraplp.Solver.OPTIMAL:
            return 'INFEASIBLE'
        output = ['{:.2f}'.format(x.solution_value()) for x in self.variables]
        output = ','.join(output)
        output += ',Z={:.2f}'.format(self.ZMax)
        return output

    def __init__(
        self,
        num_vars : int,
        num_constraints : int,
        constraint_coeffs : list,
        bounds: list,
        objective_coeffs : list
    ):
        self.num_vars = num_vars
        self.num_constraints = num_constraints
        self.constraint_coeffs = constraint_coeffs
        self.bounds = bounds
        self.objective_coeffs = objective_coeffs
        self.status = None
        self.variables = None
        self.ZMax = -infinity
        self.solver = self.__create_solver()

    def solve(self):
        self.status = self.solver.Solve()
        self.variables = self.solver.variables()
        self.ZMax = self.solver.Objective().Value()
        return self.status

class BranchAndBoundTree:
    def __init__(self, relaxed_lp : LP):
        self.relaxed_lp = relaxed_lp
        self.left = None
        self.right = None

    def __params_from_relaxed_lp(self):
        return copy(self.relaxed_lp.num_vars),\
               copy(self.relaxed_lp.num_constraints),\
               copy(self.relaxed_lp.constraint_coeffs),\
               copy(self.relaxed_lp.bounds),\
               copy(self.relaxed_lp.objective_coeffs)

    def create_left_subproblem(self, variable, lower_bound):
        num_vars, num_constraints, constraint_coeffs, bounds, objective_coeffs = self.__params_from_relaxed_lp() 
        new_constraint = [0 for i in range(num_vars)]
        new_constraint[variable] = 1
        constraint_coeffs.append(
            new_constraint
        )
        num_constraints += 1
        bounds.append(lower_bound)
        self.left = BranchAndBoundTree(
            relaxed_lp = LP(
                num_vars,
                num_constraints,
                constraint_coeffs,
                bounds,
                objective_coeffs
            )
        )

    def create_right_subproblem(self, variable, upper_bound):
        num_vars, num_constraints, constraint_coeffs, bounds, objective_coeffs = self.__params_from_relaxed_lp() 
        new_constraint = [0 for i in range(num_vars)]
        new_constraint[variable] = -1
        constraint_coeffs.append(
            new_constraint
        )
        num_constraints += 1
        bounds.append(-upper_bound)
        self.right = BranchAndBoundTree(
            relaxed_lp = LP(
                num_vars,
                num_constraints,
                constraint_coeffs,
                bounds,
                objective_coeffs
            )
        )


class BranchAndBoundMaximizationIP:
    def __init__(self, problem : LP):
        self.optimal_solution = [None for v in range(problem.num_vars)]
        self.optimal_value = -infinity
        # criando arvore de branch and bround
        self.root_problem = BranchAndBoundTree(problem)
        # criando fila de problemas branch and bound a serem resolvidos
        self.Q = [self.root_problem]

    def __enque_problems_to_be_solved(self, node):
        def __enqueing_conditions(problem):
            status = problem.Solve()
            feasibility_condition = status == pywraplp.Solver.OPTIMAL 
            bounding_condition = problem.Objective().Value() >= self.optimal_value
            return feasibility_condition and bounding_condition

        # defino lista de nodes candidatos (a receber factiveis)
        feasible_nodes = []
        feasible_nodes_values = []

        # crio copias dos solvers da esquerda e da direita
        # para verificar quem tem as melhores condicoes
        # para otimizar o branching
        future_left_problem= node.left.relaxed_lp.future_solver
        future_right_problem= node.right.relaxed_lp.future_solver

        # se o problema da esquerda for factivel
        # e seu valor de funcao objetivo
        # for maior que o valor otimo encontrado
        # até o momento (bound)
        # faço sua inserção na lista de problemas 
        # a serem adicionados na pilha Q
        if __enqueing_conditions(future_left_problem):
            feasible_nodes.append(node.left)
            feasible_nodes_values.append(future_left_problem.Objective().Value())

        # se o problema da direita for factivel
        # e seu valor de funcao objetivo
        # for maior que o valor otimo encontrado
        # até o momento (bound)
        # faço sua inserção na lista de problemas 
        # a serem adicionados na pilha Q
        if __enqueing_conditions(future_right_problem):
            feasible_nodes.append(node.right)
            feasible_nodes_values.append(future_right_problem.Objective().Value())

        # defino uma funcao de ordenacao para ordenar feasible solutions
        # pelo valor da funcao objetivo, de forma que o que tiver
        # maior valor de objetivo seja resolvido primeiro
        sort_by_objective_value = lambda x: x[1]
        nodes_to_enqueue = [
            node for node, node_value in sorted(
                zip(
                    feasible_nodes, feasible_nodes_values
                ),
                key = sort_by_objective_value
            )
        ]
        #nodes_to_enqueue = feasible_nodes
        # enfileiro os subproblemas para serem resolvidos
        # resolvendo primeiro os que tiverem maior
        # valor objetivo
        self.Q += nodes_to_enqueue

    def solve(self):
        # iterando na fila de problemas até que tenhamos resolvido todos
        end = datetime.now() + timedelta(seconds = TIME_LIMIT)
        while len(self.Q) > 0 and datetime.now() < end:
            # seleciono (e removo) o problema do topo da fila para ser resolvido
            node = self.Q.pop()
            # resolvo este problema
            node.relaxed_lp.solve()
            # se o problema não for factivel, descarto ele da minha pilha
            if node.relaxed_lp.status != pywraplp.Solver.OPTIMAL:
                continue
            # avalio se as solucoes do solver respeitam a restrição
            # de integridade inteira 
            if all_variables_are_integer(node.relaxed_lp.variables):
            # se o valor da funcao objetivo
            # do solver atual é maior que o valor otimo até o momento
            # atualizo o valor otimo
                if node.relaxed_lp.ZMax > self.optimal_value:
                    self.optimal_value = node.relaxed_lp.ZMax
                    for i in range(len(node.relaxed_lp.variables)):
                        self.optimal_solution[i] = node.relaxed_lp.variables[i].solution_value()
            # se não respeitam a restrição de integridade
            # seleciono a primeira variavel que viola a restricao
            # para particionar (branch) o problema
            else:
                variable, lower_bound = pick_variable_and_return_its_lower_bound(node.relaxed_lp.variables)
                upper_bound = lower_bound + 1
                # crio subproblema a esquerda
                # adicionando a restricao variable <= lower_bound
                node.create_left_subproblem(variable, lower_bound)
                # crio subproblema a direita
                # adicionando a restricao variable >= upper_bound
                node.create_right_subproblem(variable, upper_bound)
                # para otimizar o branch and bound, adiciono na pilha de problemas
                # o problema com menor valor, para em sequencia adicionar o de
                # maior valor, que vai ser processado primeiro
                self.__enque_problems_to_be_solved(node)
