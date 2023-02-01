import os

from constants import PROBLEMS, PROBLEM_DIMENSIONS


def print_parameters(args):
    if args.verbose:
        print()
        print('Parameters')
        print()

        for key in args.__dict__.keys():
            print(key.ljust(args.verbose_interspace), args.__dict__[key])
        print()


def check_args(args):

    if args.max_iter is not None:
        assert args.max_iter > 0
    if args.max_time is not None:
        assert args.max_time > 0
    if args.max_f_evals is not None:
        assert args.max_f_evals > 0

    assert args.verbose_interspace >= 1
    assert args.plot_dpi >= 1

    assert -1 <= args.gurobi_method <= 5

    assert args.IFSD_theta_tol <= 0
    assert 0 <= args.IFSD_qth_quantile <= 1

    assert args.ALS_alpha_0 > 0
    assert 0 < args.ALS_delta < 1
    assert 0 < args.ALS_beta < 1
    assert args.ALS_min_alpha > 0


def args_preprocessing(args):
    check_args(args)

    algorithms_names = []

    if 'IFSD' in args.algs:
        algorithms_names.append('IFSD')

    if len(algorithms_names) == 0:
        raise Exception('You must insert a set of algorithms')

    problems = []
    n_problems = 0

    if 'MAN' in args.probs:
        problems.extend(PROBLEMS['MAN'])
        for problem in PROBLEMS['MAN']:
            n_problems += len(PROBLEM_DIMENSIONS[problem.family_name()])

    if 'JOS' in args.probs:
        problems.extend(PROBLEMS['JOS'])
        for problem in PROBLEMS['JOS']:
            n_problems += len(PROBLEM_DIMENSIONS[problem.family_name()])

    if len(problems) == 0:
        raise Exception('You must insert a set of test problems')

    general_settings = {'single_point_mod': args.single_point,
                        'max_iter': args.max_iter,
                        'max_time': args.max_time,
                        'max_f_evals': args.max_f_evals,
                        'verbose': args.verbose,
                        'verbose_interspace': args.verbose_interspace,
                        'plot_pareto_front': args.plot_pareto_front,
                        'plot_pareto_solutions': args.plot_pareto_solutions,
                        'general_export': args.general_export,
                        'export_pareto_solutions': args.export_pareto_solutions,
                        'plot_dpi': args.plot_dpi}

    IFSD_settings = {'theta_tol': args.IFSD_theta_tol,
                     'qth_quantile': args.IFSD_qth_quantile}

    algorithms_settings = {'IFSD': IFSD_settings}

    DDS_settings = {'gurobi_method': args.gurobi_method,
                    'gurobi_verbose': args.gurobi_verbose}

    ALS_settings = {'alpha_0': args.ALS_alpha_0,
                    'delta': args.ALS_delta,
                    'beta': args.ALS_beta,
                    'min_alpha': args.ALS_min_alpha}

    return algorithms_names, problems, n_problems, general_settings, algorithms_settings, DDS_settings, ALS_settings


def args_file_creation(date: str, args):
    if args.general_export:
        args_file = open(os.path.join('Execution_Outputs', date, 'params.csv'), 'w')
        for key in args.__dict__.keys():
            if type(args.__dict__[key]) == float:
                args_file.write('{};{}\n'.format(key, str(round(args.__dict__[key], 10)).replace('.', ',')))
            else:
                args_file.write('{};{}\n'.format(key, args.__dict__[key]))
        args_file.close()


