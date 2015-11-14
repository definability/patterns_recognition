from unittest import TestCase, main

from classes.image import MatrixPointer


class TestMatrixPointerBasicProperties(TestCase):


    def setUp(self):
        self.matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        self.lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.pointers = [MatrixPointer(self.matrix),
                         MatrixPointer(self.lst, (3, 4))]


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


    def test_get_data_transposed(self):
        a = MatrixPointer([1, 3, 5, 2, 4, 6], (2, 3), transpose=True)
        self.assertEqual(a.get_data(), [1, 2, 3, 4, 5, 6])


    def test_get_data_transposed_involutive(self):
        for source in [self.matrix, self.lst]:
            t = MatrixPointer(source, (4, 3), transpose=True).get_data()
            tt = MatrixPointer(t, (3, 4), transpose=True).get_data()
            self.assertEqual(tt, MatrixPointer(source, (3,4)).get_data())


    def test_split_horizontal(self):
        for pointer in self.pointers:
            top, bottom = pointer.split_horizontal(3)
            self.assertEqual(top.get_data(False), [1, 2, 3, 4, 5, 6, 7, 8, 9])
            self.assertEqual(bottom.get_data(False), [10, 11, 12])


    def test_split_vertical(self):
        for pointer in self.pointers:
            left, right = pointer.split_vertical(2)
            self.assertEqual(left.get_data(False), [1, 2, 4, 5, 7, 8, 10, 11])
            self.assertEqual(right.get_data(False), [3, 6, 9, 12])


    def test_split_horizontal_all(self):
        for pointer in self.pointers:
            top, bottom = pointer.split_horizontal(4)
            self.assertEqual(top.get_data(False), self.lst)
            self.assertEqual(bottom.get_data(False), None)
            self.assertEqual(bottom.get_size(), (0, 0))


    def test_split_vertical_all(self):
        for pointer in self.pointers:
            left, right = pointer.split_vertical(3)
            self.assertEqual(left.get_data(False), self.lst)
            self.assertEqual(right.get_data(False), None)
            self.assertEqual(right.get_size(), (0, 0))


    def test_split_horizontal_none(self):
        for pointer in self.pointers:
            top, bottom = pointer.split_horizontal(0)
            self.assertEqual(top.get_data(False), None)
            self.assertEqual(top.get_size(), (0, 0))
            self.assertEqual(bottom.get_data(False), self.lst)


    def test_split_vertical_none(self):
        for pointer in self.pointers:
            left, right = pointer.split_vertical(0)
            self.assertEqual(left.get_data(False), None)
            self.assertEqual(left.get_size(), (0, 0))
            self.assertEqual(right.get_data(False), self.lst)


    def test_split_vertical_twice(self):
        for pointer in self.pointers:
            left, right = pointer.split_vertical(2)
            left, right = left.split_vertical(1)
            self.assertEqual(right.get_data(), [2, 5, 8, 11])
            self.assertEqual(right.get_size(), (1, 4))


    def test_split_horizontal_twice(self):
        for pointer in self.pointers:
            top, bottom = pointer.split_horizontal(2)
            top, bottom = top.split_horizontal(1)
            self.assertEqual(bottom.get_data(), [4, 5, 6])
            self.assertEqual(bottom.get_size(), (3, 1))


    def test_split_vertical_twice_additional(self):
        for pointer in self.pointers:
            left, right = pointer.split_vertical(2)
            self.assertEqual(right.get_size(), (1, 4))
            self.assertEqual(right.get_data(), [3, 6, 9, 12])
            left, right = right.split_vertical(1)
            self.assertEqual(left.get_size(), (1, 4))
            self.assertEqual(left.get_data(), [3, 6, 9, 12])


    def test_split_horizontal_twice(self):
        for pointer in self.pointers:
            top, bottom = pointer.split_horizontal(2)
            self.assertEqual(bottom.get_data(), [7, 8, 9, 10, 11, 12])
            self.assertEqual(bottom.get_size(), (3, 2))
            top, bottom = bottom.split_horizontal(2)
            self.assertEqual(top.get_data(), [7, 8, 9, 10, 11, 12])
            self.assertEqual(top.get_size(), (3, 2))


    def test_map_sum(self):
        a = MatrixPointer([1, 2, 3, 4], (2, 2))
        b = MatrixPointer([4, 3, 2, 1], (2, 2))
        c = a.map(lambda x, y: x + y, b)
        self.assertEqual(c, [5]*4)


    def test_map_sub(self):
        a = MatrixPointer([1, 2, 3, 4], (2, 2))
        b = MatrixPointer([4, 3, 2, 1], (2, 2))
        c = a.map(lambda x, y: x - y, b)
        self.assertEqual(c, [-3, -1, 1, 3])


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


if __name__ == '__main__':
    main()

