from utils import *
from lia_star_solver import *
import unittest

set_vars = [x, y]


def phi(x, y):
    return x + y


class TestLinearSet(unittest.TestCase):

    # def test_example1_for3(self):
    #     A = toMacro([x == x])
    #     B = toMacro([y >= 3 - x, y >= x - 3])
    #     A.args = set_vars + [a for a in A.args if a not in set_vars]
    #     B.args = set_vars + [b for b in B.args if b not in set_vars]
    #     sls = semilinear.SLS(B, set_vars, len(B.args))
    #     sls.reduce()
    #     while sls.augment():
    #         sls.reduce()
    #         print(sls.getSLS())
    #         continue

    #     X = findSolution(A, sls)
    #     print(f"solution: {X}")
    #     if X:
    #         result = returnSolution(list(zip(A.args, X)), sls)
    #         print(f"result: {result}")

    def test_example1_for4(self):
        A = toMacro([x == x])
        B = toMacro([y >= 4 - x, y >= x - 4])
        A.args = set_vars + [a for a in A.args if a not in set_vars]
        B.args = set_vars + [b for b in B.args if b not in set_vars]
        sls = semilinear.SLS(B, set_vars, len(B.args))
        sls.reduce()
        while sls.augment():
            sls.reduce()
            print(sls.getSLS())
            continue

        X = findSolution(A, sls)
        print(f"solution: {X}")
        if X:
            result = returnSolution(list(zip(A.args, X)), sls)
            print(f"result: {result}")


if __name__ == "__main__":
    unittest.main()
