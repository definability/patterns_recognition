from unittest import TestCase, main

from classes.semiring import semirings


class TestSemiringsBasicProperties(TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_zero(self):
        [S.zero() for S in semirings]


    def test_unity(self):
        [S.unity() for S in semirings]

    def test_eq(self):
        for S in semirings:
            self.assertEqual(S.zero(), S.zero())
            self.assertIsNot(S.zero(), S.zero())
            self.assertEqual(S.unity(), S.unity())
            self.assertIsNot(S.unity(), S.unity())

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

    def test_zero_add_unity(self):
        for S in semirings:
            self.assertEqual(S.zero() + S.unity(), S.unity())
            self.assertEqual(S.unity() + S.zero(), S.unity())


if __name__ == '__main__':
    main()

