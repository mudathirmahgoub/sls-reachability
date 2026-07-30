from utils import *
from lia_star_solver import *
import unittest

set_vars = [x,y]

def phi(x, y):
    return x + y

class TestLinearSet(unittest.TestCase):    

    def test_formula_2020(self):
        A = toMacro([m == m])
        B = toMacro([m == L - s, s <= m])
        set_vars = [m, L, s]
        A.args = set_vars + [a for a in A.args if a not in set_vars]
        B.args = set_vars + [b for b in B.args if b not in set_vars]
        sls = semilinear.SLS(B, set_vars, len(B.args))
        sls.reduce()
        while sls.augment():
            print(f'sls before: {sls.getSLS()}')
            sls.reduce()
            print(f'sls after: {sls.getSLS()}')
            # print(sls.getSLS())
            continue
        
        X = findSolution(A, sls)
        print(f"solution: {X}")
        if X: 
            result = returnSolution(list(zip(A.args, X)), sls)
            print(f"result: {result}")



if __name__ == "__main__":
    unittest.main()
