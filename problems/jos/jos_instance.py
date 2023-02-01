import numpy as np
import tensorflow as tf

from problems.jos.jos_class import JOS

'''
For more details about the JOS problem, the user is referred to 

Jin, Y., Olhofer, M., Sendhoff, B.: Dynamic weighted aggregation for evo-
lutionary multi-objective optimization: Why does it work and how? In:
Proceedings of the Genetic and Evolutionary Computation Conference,
pp. 1042–1049 (2001).
'''

class MJOS(JOS):

    def __init__(self, n: int):
        assert n >= 1

        JOS.__init__(self, n)

        self.objectives = [
            tf.reduce_sum([self._z[i] ** 2 for i in range(self.n)]) / self.n,
            tf.reduce_sum([(self._z[i] - 2) ** 2 for i in range(self.n)]) / self.n
        ]

        self.filtered_lb_for_ini = -100 * np.ones(self.n)
        self.filtered_ub_for_ini = 100 * np.ones(self.n)

    @staticmethod
    def name():
        return 'MJOS'
