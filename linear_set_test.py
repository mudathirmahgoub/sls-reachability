from utils import *
from lia_star_solver import *
import unittest

set_vars = [x,y]

def phi(x, y):
    return x + y

class TestLinearSet(unittest.TestCase):    

    def test_formula(self):
        A = toMacro([x == x])
        B = toMacro([x == 1, y >= 1])
        A.args = set_vars + [a for a in A.args if a not in set_vars]
        B.args = set_vars + [b for b in B.args if b not in set_vars]
        sls = semilinear.SLS(B, set_vars, len(B.args))
        sls.reduce()
        while sls.augment():
            print(sls.getSLS())
            continue
        
        X = findSolution(A, sls)
        print(f"solution: {X}")
        if X: returnSolution(list(zip(A.args, X)), sls)


if __name__ == "__main__":
    unittest.main()
