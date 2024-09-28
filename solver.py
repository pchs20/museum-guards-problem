from typing import Optional

from pyomo.environ import ConcreteModel, SolverFactory, SolverStatus, value
from pyomo.opt.results import SolverResults


class Solver:
    def __init__(self, concrete_model: ConcreteModel):
        self.concrete_model: ConcreteModel = concrete_model
        self._solution: Optional[SolverResults] = None

    def solve(self) -> None:
        solver = SolverFactory('scip')
        solver.options['limits/time'] = 300
        self._solution = solver.solve(self.concrete_model, tee=True)

    def solution_exists(self) -> bool:
        solution_found = (
            self._solution.solver.status == SolverStatus.ok or
            self._solution.solver.status == SolverStatus.warning
        )
        return solution_found

    def print_solution(self) -> None:
        assert self.solution_exists(), 'The solver did not find any solution!'

        print()
        print('SOLUTION')
        number_of_guards = int(value(self.concrete_model.objective_function))
        print('Number of guards needed: ' + str(number_of_guards))
        print('Where to put the guards: ')
        for door in self.concrete_model.doors:
            guard_at_door = bool(self.concrete_model.guard_at_door[door].value)
            print(str(door) + ': ' + str(guard_at_door))
        print()
