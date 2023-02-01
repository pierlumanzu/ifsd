from algorithms.gradient_based.ifsd import IFSD


class AlgorithmFactory:

    @staticmethod
    def get_algorithm(algorithm_name: str, **kwargs):

        general_settings = kwargs['general_settings']
        algorithms_settings = kwargs['algorithms_settings']

        if algorithm_name == 'IFSD':
            IFSD_settings = algorithms_settings[algorithm_name]

            DDS_settings = kwargs['DDS_settings']
            ALS_settings = kwargs['ALS_settings']

            return IFSD(general_settings['max_iter'],
                             general_settings['max_time'],
                             general_settings['max_f_evals'],
                             general_settings['verbose'],
                             general_settings['verbose_interspace'],
                             general_settings['plot_pareto_front'],
                             general_settings['plot_pareto_solutions'],
                             general_settings['plot_dpi'],
                             IFSD_settings['theta_tol'],
                             IFSD_settings['qth_quantile'],
                             DDS_settings['gurobi_method'],
                             DDS_settings['gurobi_verbose'],
                             ALS_settings['alpha_0'],
                             ALS_settings['delta'],
                             ALS_settings['beta'],
                             ALS_settings['min_alpha'])

        else:
            raise NotImplementedError
