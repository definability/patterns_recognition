from unittest import TestCase, main

from classes.image import MatrixPointer


class TestMatrixPointerBasicProperties(TestCase):


    def setUp(self):
        self.matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        self.lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.pointers = [MatrixPointer(self.matrix),
                         MatrixPointer(self.lst, (3, 3))]


    def tearDown(self):
        del self.matrix
        del self.lst
        del self.pointers


    def test_constructor(self):
        for pointer in self.pointers:
            self.assertIsInstance(pointer, MatrixPointer)


    def test_get_data(self):
        for pointer in self.pointers:
            self.assertEqual(pointer.get_data(True), self.lst)

    def test_split_horizontal(self):
        for pointer in self.pointers:
            top, bottom = pointer.split_horizontal(3)
            self.assertEqual(top.get_data(False),
                             ([1, 2, 3, 4, 5, 6, 7, 8, 9]))
            self.assertEqual(bottom.get_data(False),
                             ([10, 11, 12]))


    def test_split_vertical(self):
        for pointer in self.pointers:
            left, right = pointer.split_vertical(2)
            self.assertEqual(left.get_data(False),
                             ([1, 2, 4, 5, 7, 8, 10, 11]))
            self.assertEqual(right.get_data(False),
                             ([3, 6, 9, 12]))


    def test_map_sum(self):
        a = MatrixPointer([1, 2, 3, 4], (2, 2))
        b = MatrixPointer([4, 3, 2, 1], (2, 2))
        c = a.map(lambda x, y: x + y, b)
        self.assertEqual(c, [5]*4)


    def test_reduce_sum(self):
        a = MatrixPointer([1, 2, 3, 4], (2, 2))
        b = MatrixPointer([4, 3, 2, 1], (2, 2))
        c = a.reduce(lambda accumulator, x, y: accumulator + x + y, 0, b)
        self.assertEqual(c, sum([5]*4))


    def test_reduce_sqr_diff(self):
        a = MatrixPointer([1, 2, 3, 4], (2, 2))
        b = MatrixPointer([4, 3, 2, 1], (2, 2))
        c = a.reduce(lambda accumulator, x, y: accumulator + (x - y)**2, 0, b)
        self.assertEqual(c, 20)


    def test_sub(self):
        a = MatrixPointer([1, 2, 3, 4], (2, 2))
        b = MatrixPointer([4, 3, 2, 1], (2, 2))
        c = a - b
        self.assertEqual(c, [-3, -1, 1, 3])


if __name__ == '__main__':
    main()

