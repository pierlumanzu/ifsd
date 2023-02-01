from datetime import datetime
import numpy as np
import tensorflow as tf

from nsma.algorithms.algorithm_utils.graphical_plot import GraphicalPlot
from nsma.general_utils.pareto_utils import points_initialization

from algorithms.algorithm_factory import AlgorithmFactory
from general_utils.args_utils import print_parameters, args_preprocessing, args_file_creation
from general_utils.management_utils import folder_initialization, execution_time_file_initialization, write_in_execution_time_file, write_results_in_csv_file, save_plots
from general_utils.pareto_utils import points_postprocessing
from general_utils.progress_bar import ProgressBarWrapper
from constants import PROBLEM_DIMENSIONS
from parser_management import get_args

tf.compat.v1.disable_eager_execution()

args = get_args()

print_parameters(args)
algorithms_names, problems, n_problems, general_settings, algorithms_settings, DDS_settings, ALS_settings = args_preprocessing(args)
print('N° algorithms: ', len(algorithms_names))
print('N° problems: ', n_problems)
print('Initial solution(s): ', 'n points uniformly sampled from the hyper-diagonal' if not general_settings['single_point_mod'] else 'midpoint of the hyper-diagonal')
print()

date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

if general_settings['verbose']:
    progress_bar = ProgressBarWrapper(len(algorithms_names) * n_problems)
    progress_bar.show_bar()

if general_settings['general_export']:
    folder_initialization(date, algorithms_names)
    args_file_creation(date, args)
    execution_time_file_initialization(date, algorithms_names)

for problem in problems:
    print()
    print('Problem: ', problem.name())

    var_range = PROBLEM_DIMENSIONS[problem.family_name()]

    for n in var_range:
        print()
        print()
        print('N: ', n)

        for algorithm_name in algorithms_names:
            print()
            print('Algorithm: ', algorithm_name)

            session = tf.compat.v1.Session()
            with session.as_default():

                problem_instance = problem(n=n)

                initial_p_list, initial_f_list, n_initial_points = points_initialization(problem_instance, 'hyper', n if not general_settings['single_point_mod'] else 1)

                algorithm = AlgorithmFactory.get_algorithm(algorithm_name,
                                                           general_settings=general_settings,
                                                           algorithms_settings=algorithms_settings,
                                                           DDS_settings=DDS_settings,
                                                           ALS_settings=ALS_settings)

                p_list, f_list, elapsed_time = algorithm.search(np.copy(initial_p_list), np.copy(initial_f_list), problem_instance)

                p_list, f_list = points_postprocessing(np.copy(p_list), np.copy(f_list), problem_instance)

                if general_settings['plot_pareto_front']:
                    graphical_plot = GraphicalPlot(general_settings['plot_pareto_solutions'], general_settings['plot_dpi'])
                    graphical_plot.show_figure(p_list, f_list, hold_still=True)
                    graphical_plot.close_figure()

                if general_settings['general_export']:
                    write_in_execution_time_file(date, algorithm_name, problem, n, elapsed_time)
                    write_results_in_csv_file(p_list, f_list, date, algorithm_name, problem, export_pareto_solutions=general_settings['export_pareto_solutions'])
                    save_plots(p_list, f_list, date, algorithm_name, problem, general_settings['export_pareto_solutions'], general_settings['plot_dpi'])

                if general_settings['verbose']:
                    progress_bar.increment_current_value()
                    progress_bar.show_bar()

                tf.compat.v1.reset_default_graph()
                session.close()
