from direction_solvers.descent_direction.steepest_descent_ds_gurobi_version import SteepestDescentDSGurobiVersion


class DirectionSolverFactory:

    @staticmethod
    def get_direction_calculator(direction_type: str, gurobi_method: int, gurobi_verbose: bool):

        if direction_type == 'Steepest_Descent_DS':
            return SteepestDescentDSGurobiVersion(gurobi_method, gurobi_verbose)
        else:
            raise NotImplementedError
