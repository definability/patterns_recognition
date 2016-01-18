from unittest import TestCase, main

from classes.semiring import semirings
from classes.semiring.SemiringElement import SemiringElement


class TestSemiringBasicProperties(TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_instance(self):
        [self.assertIsInstance(S(), SemiringElement) for S in semirings]


    def test_zero(self):
        [S.zero() for S in semirings]


    def test_unity(self):
        [S.unity() for S in semirings]


    def test_not_implemented_nulary_methods(self):
        s = SemiringElement(0)
        for method in ['unity', 'zero']:
            with self.assertRaises(NotImplementedError):
                getattr(s, method)()


    def test_not_implemented_unary_methods(self):
        a = SemiringElement(0)
        b = SemiringElement(1)
        for method in ['add', 'mul']:
            with self.assertRaises(NotImplementedError):
                getattr(a, method)(b)


    def test_str(self):
        for S in semirings:
            self.assertEqual(str(S()), str(S.zero()))
            self.assertEqual(repr(S()), repr(S.zero()))


    def test_eq(self):
        for S in semirings:
            self.assertEqual(S.zero(), S.zero())
            self.assertIsNot(S.zero(), S.zero())
            self.assertEqual(S.unity(), S.unity())
            self.assertIsNot(S.unity(), S.unity())


    def test_neq(self):
        for S in semirings:
            self.assertTrue(S.zero(), S.unity())


    def test_zero_add_zero(self):
        for S in semirings:
            self.assertEqual(S.zero() + S.zero(), S.zero())


    def test_unity_mul_unity(self):
        for S in semirings:
            self.assertEqual(S.unity() * S.unity(), S.unity())


    def test_zero_mul_unity(self):
        for S in semirings:
            self.assertEqual(S.zero() * S.unity(), S.zero())
            self.assertEqual(S.unity() * S.zero(), S.zero())


    def test_imul(self):
        for S in semirings:
            unity = S.unity()
            zero = S.zero()
            zero *= unity
            self.assertEqual(zero, S.zero())


    def test_iadd(self):
        for S in semirings:
            unity = S.unity()
            zero = S.zero()
            unity += zero
            self.assertEqual(unity, S.unity())


    def test_zero_add_unity(self):
        for S in semirings:
            self.assertEqual(S.zero() + S.unity(), S.unity())
            self.assertEqual(S.unity() + S.zero(), S.unity())


if __name__ == '__main__':
    main()

