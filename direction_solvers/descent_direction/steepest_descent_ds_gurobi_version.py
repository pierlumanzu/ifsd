import numpy as np
from gurobipy import Model, GRB

from nsma.direction_solvers.descent_direction.dds import DDS
from nsma.direction_solvers.gurobi_settings import GurobiSettings

from nsma.problems.problem import Problem


class SteepestDescentDSGurobiVersion(DDS, GurobiSettings):

    def __init__(self, gurobi_method: int, gurobi_verbose: bool):
        DDS.__init__(self)
        GurobiSettings.__init__(self, gurobi_method, gurobi_verbose)

    def compute_direction(self, problem: Problem, Jac: np.array, x_p: np.array= None):
        assert x_p is not None

        m, n = Jac.shape

        if np.isinf(Jac).any() or np.isnan(Jac).any():
            return np.zeros(n), 0

        try:
            model = Model("Steepest Descent Direction")
            model.setParam("OutputFlag", self._gurobi_verbose)
            model.setParam("Method", self._gurobi_method)

            z = model.addMVar(n, lb=-np.inf, ub=np.inf, name="z")
            beta = model.addMVar(1, lb=-np.inf, ub=0., name="beta")

            obj = beta - (x_p @ z) + 1/2 * (z @ z) + 1/2 * (x_p @ x_p)
            model.setObjective(obj)

            for j in range(m):
                model.addConstr(Jac[j, :] @ z <= beta + Jac[j, :] @ x_p, name='Jacobian constraint n°{}'.format(j))

            model.update()

            for i in range(n):
                z[i].start = float(x_p[i])
            beta.start = 0.

            model.optimize()

            if model.Status == GRB.OPTIMAL:
                sol = model.getVars()

                d_p = np.array([s.x for s in sol][:n]) - x_p
                theta_p = model.getObjective().getValue()

            else:
                return np.zeros(n), 0

        except AttributeError:
            return np.zeros(n), 0

        return d_p, theta_p
