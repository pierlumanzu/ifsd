import time
import numpy as np

from nsma.algorithms.genetic.genetic_utils.general_utils import calc_crowding_distance
from nsma.general_utils.pareto_utils import pareto_efficient

from algorithms.gradient_based.extended_gradient_based_algorithm import ExtendedGradientBasedAlgorithm
from line_searches.line_search_factory import LineSearchFactory
from problems.extended_problem import ExtendedProblem


class IFSD(ExtendedGradientBasedAlgorithm):

    def __init__(self,
                 max_iter: int, max_time: float, max_f_evals: int,
                 verbose: bool, verbose_interspace: int,
                 plot_pareto_front: bool, plot_pareto_solutions: bool, plot_dpi: int,
                 theta_tol: float, qth_quantile: float,
                 gurobi_method: int, gurobi_verbose: bool,
                 ALS_alpha_0: float, ALS_delta: float, ALS_beta: float, ALS_min_alpha: float):

        ExtendedGradientBasedAlgorithm.__init__(self,
                                                max_iter, max_time, max_f_evals,
                                                verbose, verbose_interspace,
                                                plot_pareto_front, plot_pareto_solutions, plot_dpi,
                                                theta_tol,
                                                gurobi_method, gurobi_verbose,
                                                ALS_alpha_0, ALS_delta, ALS_beta, ALS_min_alpha,
                                                name_DDS='Steepest_Descent_DS', name_ALS='Boundconstrained_Front_ALS')

        self.__single_point_line_search = LineSearchFactory.get_line_search('MOALS', ALS_alpha_0, ALS_delta, ALS_beta, ALS_min_alpha)

        self.__qth_quantile = qth_quantile

    def search(self, p_list: np.array, f_list: np.array, problem: ExtendedProblem):

        self.update_stopping_condition_current_value('max_time', time.time())

        efficient_point_idx = pareto_efficient(f_list)
        f_list = f_list[efficient_point_idx, :]
        p_list = p_list[efficient_point_idx, :]

        self.show_figure(p_list, f_list)

        crowding_quantile = np.inf

        while not self.evaluate_stopping_conditions():

            self.output_data(f_list, crowding_quantile=crowding_quantile)
            self.add_to_stopping_condition_current_value('max_iter', 1)

            previous_p_list = np.copy(p_list)
            previous_f_list = np.copy(f_list)

            crowding_list = calc_crowding_distance(previous_f_list)
            is_finite_idx = np.isfinite(crowding_list)

            if len(crowding_list[is_finite_idx]) > 0:
                crowding_quantile = np.quantile(crowding_list[is_finite_idx], self.__qth_quantile)
            else:
                crowding_quantile = np.inf

            sorted_idx = np.flip(np.argsort(crowding_list))

            previous_p_list = previous_p_list[sorted_idx, :]
            previous_f_list = previous_f_list[sorted_idx, :]
            crowding_list = crowding_list[sorted_idx]

            point_idx = 0

            while not self.evaluate_stopping_conditions() and point_idx < len(previous_p_list):

                x_p = previous_p_list[point_idx, :]
                f_p = previous_f_list[point_idx, :]

                J_p = problem.evaluate_functions_jacobian(x_p)
                self.add_to_stopping_condition_current_value('max_f_evals', problem.n)

                power_set = self.objectives_powerset(problem.m)

                if self.exists_dominating_point(f_p, f_list):
                    point_idx += 1
                    continue

                common_d_p, common_theta_p = self._direction_solver.compute_direction(problem, J_p, x_p)

                if not self.evaluate_stopping_conditions() and common_theta_p < self._theta_tol:

                    new_x_p, new_f_p, _, sp_ls_f_evals = self.__single_point_line_search.search(problem, x_p, f_p, common_d_p, common_theta_p)
                    self.add_to_stopping_condition_current_value('max_f_evals', sp_ls_f_evals)

                    if not self.evaluate_stopping_conditions() and new_x_p is not None:

                        efficient_points_idx = self.fast_non_dominated_filter(f_list, new_f_p.reshape((1, problem.m)))

                        p_list = np.concatenate((p_list[efficient_points_idx, :],
                                                 new_x_p.reshape((1, problem.n))), axis=0)

                        f_list = np.concatenate((f_list[efficient_points_idx, :],
                                                 new_f_p.reshape((1, problem.m))), axis=0)

                        x_p = np.copy(new_x_p)
                        f_p = np.copy(new_f_p)

                        J_p = problem.evaluate_functions_jacobian(x_p)
                        self.add_to_stopping_condition_current_value('max_f_evals', problem.n)

                        self.show_figure(p_list, f_list)

                else:
                    power_set.remove(tuple(range(problem.m)))

                for I_k in power_set:

                    if self.evaluate_stopping_conditions() or self.exists_dominating_point(f_p, f_list) or crowding_list[point_idx] < crowding_quantile:
                        break

                    partial_d_p, partial_theta_p = self._direction_solver.compute_direction(problem, J_p[I_k, ], x_p)

                    if not self.evaluate_stopping_conditions() and partial_theta_p < self._theta_tol:

                        new_x_p, new_f_p, _, f_ls_f_evals = self._line_search.search(problem, x_p, f_list, partial_d_p, 0., I=np.arange(problem.m))
                        self.add_to_stopping_condition_current_value('max_f_evals', f_ls_f_evals)

                        if not self.evaluate_stopping_conditions() and new_x_p is not None:

                            efficient_points_idx = self.fast_non_dominated_filter(f_list, new_f_p.reshape((1, problem.m)))

                            p_list = np.concatenate((p_list[efficient_points_idx, :],
                                                     new_x_p.reshape((1, problem.n))), axis=0)

                            f_list = np.concatenate((f_list[efficient_points_idx, :],
                                                     new_f_p.reshape((1, problem.m))), axis=0)

                point_idx += 1

            self.show_figure(p_list, f_list)

        self.output_data(f_list, crowding_quantile=crowding_quantile)
        self.close_figure()

        return p_list, f_list, time.time() - self.get_stopping_condition_current_value('max_time')
