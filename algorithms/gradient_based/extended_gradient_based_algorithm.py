import numpy as np
from abc import ABC
from itertools import chain, combinations

from nsma.algorithms.gradient_based.gradient_based_algorithm import GradientBasedAlgorithm

from direction_solvers.direction_solver_factory import DirectionSolverFactory
from line_searches.line_search_factory import LineSearchFactory


class ExtendedGradientBasedAlgorithm(GradientBasedAlgorithm, ABC):

    def __init__(self,
                 max_iter: int, max_time: float, max_f_evals: int,
                 verbose: bool, verbose_interspace: int,
                 plot_pareto_front: bool, plot_pareto_solutions: bool, plot_dpi: int,
                 theta_tol: float,
                 gurobi_method: int, gurobi_verbose: bool,
                 ALS_alpha_0: float, ALS_delta: float, ALS_beta: float, ALS_min_alpha: float,
                 name_DDS: str=None, name_ALS: str=None):

        GradientBasedAlgorithm.__init__(self,
                                        max_iter, max_time, max_f_evals,
                                        verbose, verbose_interspace,
                                        plot_pareto_front, plot_pareto_solutions, plot_dpi,
                                        theta_tol,
                                        True, gurobi_method, gurobi_verbose,
                                        0., 0., 0., 0.)

        self._direction_solver = DirectionSolverFactory.get_direction_calculator(name_DDS, gurobi_method, gurobi_verbose) if name_DDS is not None else None
        self._line_search = LineSearchFactory.get_line_search(name_ALS, ALS_alpha_0, ALS_delta, ALS_beta, ALS_min_alpha) if name_ALS is not None else None

    @staticmethod
    def objectives_powerset(m: int):
        s = list(range(m))
        return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))

    @staticmethod
    def exists_dominating_point(f: np.array, f_list: np.array):

        if np.isnan(f).any():
            return True

        n_obj = len(f)

        f = np.reshape(f, (1, n_obj))
        dominance_matrix = f_list - f

        return (np.logical_and(np.sum(dominance_matrix <= 0, axis=1) == n_obj, np.sum(dominance_matrix < 0, axis=1) > 0)).any()
