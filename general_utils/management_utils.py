import os
import numpy as np

from nsma.algorithms.algorithm_utils.graphical_plot import GraphicalPlot

from problems.extended_problem import ExtendedProblem


def make_folder(folder_path: str):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def folder_initialization(date: str, algorithms_names: list):
    assert os.path.exists(os.path.join('Execution_Outputs'))

    folders = ['Execution_Times', 'Csv', 'Plot']

    path = os.path.join('Execution_Outputs', date)
    make_folder(path)

    for index_folder, folder in enumerate(folders):
        make_folder(os.path.join(path, folder))
        if index_folder >= 1:
            for algorithm_name in algorithms_names:
                make_folder(os.path.join(path, folder, algorithm_name))


def execution_time_file_initialization(date: str, algorithms_names: list):
    for algorithm_name in algorithms_names:
        execution_time_file = open(os.path.join('Execution_Outputs', date, 'Execution_Times', '{}.txt'.format(algorithm_name)), 'w')
        execution_time_file.close()


def write_in_execution_time_file(date: str, algorithm_name: str, problem: ExtendedProblem, n: int, elapsed_time: float):
    execution_time_file = open(os.path.join('Execution_Outputs', date, 'Execution_Times', '{}.txt'.format(algorithm_name)), 'a')
    execution_time_file.write('Problem: ' + problem.__name__ + '    N: ' + str(n) + '    Time: ' + str(elapsed_time) + '\n')
    execution_time_file.close()


def write_results_in_csv_file(p_list: np.array, f_list: np.array, date: str, algorithm_name: str, problem: ExtendedProblem, export_pareto_solutions: bool=False):
    assert len(p_list) == len(f_list)
    n = p_list.shape[1]

    f_list_file = open(os.path.join('Execution_Outputs', date, 'Csv', algorithm_name, '{}_{}_pareto_front.csv'.format(problem.__name__, n)), 'w')
    if len(f_list):
        for i in range(f_list.shape[0]):
            f_list_file.write(';'.join([str(el) for el in f_list[i, :]]) + '\n')
    f_list_file.close()

    if export_pareto_solutions:
        p_list_file = open(os.path.join('Execution_Outputs', date, 'Csv', algorithm_name, '{}_{}_pareto_solutions.csv'.format(problem.__name__, n)), 'w')
        if len(p_list):
            for i in range(p_list.shape[0]):
                p_list_file.write(';'.join([str(el) for el in p_list[i, :]]) + '\n')
        p_list_file.close()


def save_plots(p_list: np.array, f_list: np.array, date: str, algorithm_name: str, problem: ExtendedProblem, export_pareto_solutions: bool, plot_dpi: int):
    assert len(p_list) == len(f_list)

    graphical_plot = GraphicalPlot(export_pareto_solutions, plot_dpi)
    graphical_plot.save_figure(p_list, f_list, os.path.join('Execution_Outputs', date, 'Plot'), algorithm_name, problem.__name__)
