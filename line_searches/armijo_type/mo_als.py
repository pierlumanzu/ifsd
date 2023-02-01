import numpy as np

from nsma.line_searches.armijo_type.als import ALS

from problems.extended_problem import ExtendedProblem


class MOALS(ALS):

    def __init__(self, alpha_0: float, delta: float, beta: float, min_alpha: float):
        ALS.__init__(self, alpha_0, delta, beta, min_alpha)

    def search(self, problem: ExtendedProblem, x: np.array, f: np.array, d: np.array, theta: float, I: np.array=None):
        assert len(f.shape) == 1
        assert I is None

        alpha = self._alpha_0
        new_x = x + alpha * d
        new_f = problem.evaluate_functions(new_x)
        f_eval = 1

        while (np.isnan(new_f).any() or np.isinf(new_f).any() or np.any(new_f >= f + self._beta * alpha * theta)) and alpha > self._min_alpha:
            alpha *= self._delta
            new_x = x + alpha * d
            new_f = problem.evaluate_functions(new_x)
            f_eval += 1

        if alpha <= self._min_alpha:
            alpha = 0
            return None, None, alpha, f_eval

        return new_x, new_f, alpha, f_eval