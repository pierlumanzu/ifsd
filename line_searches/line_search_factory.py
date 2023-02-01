from nsma.line_searches.armijo_type.boundconstrained_front_als import BoundconstrainedFrontALS

from line_searches.armijo_type.mo_als import MOALS


class LineSearchFactory:

    @staticmethod
    def get_line_search(line_search_type: str, alpha_0: float, delta: float, beta: float, min_alpha: float):

        if line_search_type == 'Boundconstrained_Front_ALS':
            return BoundconstrainedFrontALS(alpha_0, delta, beta, min_alpha)

        elif line_search_type == 'MOALS':
            return MOALS(alpha_0, delta, beta, min_alpha)

        else:
            raise NotImplementedError
