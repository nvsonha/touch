from sage.all import *


class ScalarSol():
    def __init__(self, m, q_s):
        self.m = m              # Number of messages = h = m
        self.q_s = q_s          # Finite field of order q_s
        self.Fqs = GF(q_s)      # Finite field
        self.Fqsm = GF(q_s**m)  # Extention field of order q_s^m
        self.C = []             # List of all vectorized elements

    def generate_possible_messages(self):
        """
        This is used to show all 1-dimensional subspace over Fq^m
        :return: List of all vectorized elements over GF(q) in column display
        """
        for x in self.Fqsm:
            A = Matrix(self.Fqs, self.m, 1)
            A[:,0] = x._vector_()
            self.C.append(A)
        return self.C




