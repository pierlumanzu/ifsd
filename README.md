[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3106/)
[![license](https://img.shields.io/badge/license-apache_2.0-orange.svg)](https://opensource.org/licenses/Apache-2.0)
[![DOI](https://zenodo.org/badge/596107659.svg)](https://zenodo.org/badge/latestdoi/596107659)

<p>
  <img src="README_Front_Image_1.gif" width="49%" />
  <img src="README_Front_Image_2.gif" width="49%" /> 
</p>

## IFSD: Improved Front Steepest Descent for Multi-Objective Optimization

Implementation of the IFSD Algorithm proposed in

[Lapucci, M. & Mansueto, P., Improved front steepest descent for multi-objective optimization. Operations Research Letters (2023).](
https://doi.org/10.1016/j.orl.2023.03.001)

If you have used our code for research purposes, please cite the publication mentioned above.
For the sake of simplicity, we provide the Bibtex format:

```
@article{LAPUCCI2023242,
    title = {Improved front steepest descent for multi-objective optimization},
    journal = {Operations Research Letters},
    volume = {51},
    number = {3},
    pages = {242-247},
    year = {2023},
    issn = {0167-6377},
    doi = {https://doi.org/10.1016/j.orl.2023.03.001},
    url = {https://www.sciencedirect.com/science/article/pii/S0167637723000433},
    author = {Matteo Lapucci and Pierluigi Mansueto},
    keywords = {Multi-objective optimization, Steepest descent, Pareto front}
}

```

### Main Dependencies Installation

In order to execute the code, you need an [Anaconda](https://www.anaconda.com/) environment and the Python package [nsma](https://pypi.org/project/nsma/) installed in it. For a detailed documentation of this framework, we refer the reader to its [GitHub repository](https://github.com/pierlumanzu/nsma).

For the package installation, open a terminal (Anaconda Prompt for Windows users) in the project root folder and execute the following command. Note that a Python version 3.10.6 or higher is required.

```
pip install nsma
```

##### Gurobi Optimizer

In order to run some parts of the code, the [Gurobi](https://www.gurobi.com/) Optimizer needs to be installed and, in addition, a valid Gurobi licence is required.

### Usage

In ```parser_management.py``` you can find all the possible arguments. Given a terminal (Anaconda Prompt for Windows users), an example of execution could be the following.

```python main.py --algs IFSD --probs MAN --max_time 2 --plot_pareto_front --plot_pareto_solutions --general_export --export_pareto_solutions```

### Contact

If you have any question, feel free to contact me:

[Pierluigi Mansueto](https://webgol.dinfo.unifi.it/pierluigi-mansueto/)<br>
Global Optimization Laboratory ([GOL](https://webgol.dinfo.unifi.it/))<br>
University of Florence<br>
Email: pierluigi dot mansueto at unifi dot it
