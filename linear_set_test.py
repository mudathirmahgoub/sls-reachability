from utils import *

import unittest


class TestLinearSet(unittest.TestCase):
    def test_size(self):
        with self.assertRaises(AssertionError):
            _ = LinearSet([c6, c7], [[c1, c2], [c4, c5, c6]])

    def test_linear_combination_const(self):
        linear_set = LinearSet([c6, c7, c8], [[c1, c2, c3], [c4, c5, c6]])
        (lambdas, linear_combination) = linear_set.linear_combination_const()
        self.assertEqual("[lambda_0, lambda_1]", str(lambdas))
        self.assertTrue(
            "[(+ (+ 0 (* lambda_0 1)) (* lambda_1 4)), (+ (+ 0 (* lambda_0 2)) (* lambda_1 5)), (+ (+ 0 (* lambda_0 3)) (* lambda_1 6))]",
            str(linear_combination),
        )

    def test_get_const(self):
        linear_set = LinearSet([c6, c7, c8], [[c1, c2, c3], [c4, c5, c6]])
        const_linear_set = linear_set.get_const()
        self.assertEqual(
            ConstantLinearSet([6, 7, 8], [[1, 2, 3], [4, 5, 6]]), const_linear_set
        )

    def test_shift_down(self):
        linear_set = LinearSet([c4, c4, c4], [[c1, c2, c3], [c4, c5, c6]])
        actual = linear_set.shift_down([x, y, z], true)
        expected = LinearSet([c3, c2, c1], [[c1, c2, c3], [c4, c5, c6]])
        self.assertEqual(expected, actual)

    def test_merge(self):
        linear_set1 = LinearSet([c1, c1], [[c2, c3], [c4, c5]])
        linear_set2 = LinearSet([c0, c0], [[c6, c7], [c8, c9]])
        actual, modified = LinearSet.merge(linear_set1, linear_set2, [x, y], true)
        expected = LinearSet(
            [c0, c0], [[c2, c3], [c4, c5], [c6, c7], [c8, c9], [c1, c1]]
        )
        self.assertTrue(modified)
        self.assertEqual(expected, actual)

    def test_offset_down(self):
        linear_set = LinearSet([c4, c4, c4], [[c1, c2, c3], [c4, c5, c6]])
        actual = linear_set.offset_down([x, y, z], true)
        expected = LinearSet([c4, c4, c4], [[c1, c2, c3], [c3, c3, c3]])
        self.assertEqual(expected, actual)


class TestSaturate(unittest.TestCase):
    def test_saturate(self):
        U = [
            LinearSet([c1, c1], [[c2, c3], [c4, c5]]),
            LinearSet([c0, c0], [[c6, c7], [c8, c9]]),
        ]
        saturate(U, [x, y], true)


class TestLIA2SLS(unittest.TestCase):
    def test_LIA2SLS_f2(self):
        # 5x + 2y >= 17
        constraint21 = tm.mkTerm(
            Kind.GEQ,
            tm.mkTerm(
                Kind.ADD, tm.mkTerm(Kind.MULT, c5, x), tm.mkTerm(Kind.MULT, c2, y)
            ),
            c17,
        )
        # 3x − y <= 8
        constraint22 = tm.mkTerm(
            Kind.LEQ, tm.mkTerm(Kind.SUB, tm.mkTerm(Kind.MULT, c3, x), y), c8
        )
        # 2x + 3y <= 20
        constraint23 = tm.mkTerm(
            Kind.LEQ,
            tm.mkTerm(
                Kind.ADD, tm.mkTerm(Kind.MULT, c2, x), tm.mkTerm(Kind.MULT, c3, y)
            ),
            c20,
        )
        # F2 formula
        f2 = constraint21.andTerm(constraint22).andTerm(constraint23)
        sls = LIA2SLS([x, y], f2)
        print(sls)


class TestLIA2SLS(unittest.TestCase):
    def test_LIA2SLS_f1(self):
        # y + 2x >= 17
        constraint11 = tm.mkTerm(
            Kind.GEQ, tm.mkTerm(Kind.ADD, y, tm.mkTerm(Kind.MULT, c2, x)), c17
        )
        # 6x − y <= 47
        constraint12 = tm.mkTerm(
            Kind.LEQ, tm.mkTerm(Kind.SUB, tm.mkTerm(Kind.MULT, c6, x), y), c47
        )
        # F1 formula
        f1 = constraint11.andTerm(constraint12)
        sls = LIA2SLS([x, y], f1)
        print(sls)

    def test_LIA2SLS_true(self):
        sls = LIA2SLS([x, y], true)
        print(sls)

    def test_LIA2SLS_geq_one(self):
        # x >= 1
        constraint1 = tm.mkTerm(Kind.GEQ, x, c1)
        # y >= 1
        constraint2 = tm.mkTerm(Kind.GEQ, y, c1)
        # F1 formula
        f = constraint1.andTerm(constraint2)
        sls = LIA2SLS([x, y], f)
        print(sls)

    def test_LIA2SLS_x_geq_one(self):
        # x >= 1
        f = tm.mkTerm(Kind.GEQ, x, c1)
        sls = LIA2SLS([x, y], f)
        print(sls)


if __name__ == "__main__":
    unittest.main()
