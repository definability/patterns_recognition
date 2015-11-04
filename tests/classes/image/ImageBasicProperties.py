from unittest import TestCase, main

from classes.image import Image


class TestImageBasicProperties(TestCase):


    def setUp(self):
        self.matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.images = [Image([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                       Image([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)]


    def tearDown(self):
        del self.matrix
        del self.images


    def test_constructor(self):
        for image in self.images:
            self.assertIsInstance(image, Image)


    def test_get_matrix(self):
        for image in self.images:
            self.assertEqual(image.get_matrix().tolist(), self.matrix)


    def test_crop_horizontal(self):
        for image in self.images:
            self.assertEqual(image.crop_horizontal(2, 1).tolist(),
                             [[4, 5, 6], [7, 8, 9]])


    def test_crop_vertical(self):
        for image in self.images:
            self.assertEqual(image.crop_vertical(2, 1).tolist(),
                             [[2, 3], [5, 6], [8, 9]])


    def test_split_horizontal(self):
        for image in self.images:
            splitted = image.split_horizontal(2)
            self.assertEqual(splitted[0].tolist(),
                             ([[1, 2, 3], [4, 5, 6]]))
            self.assertEqual(splitted[1].tolist(),
                             ([[7, 8, 9]]))


    def test_split_vertical(self):
        for image in self.images:
            splitted = image.split_vertical(2)
            self.assertEqual(splitted[0].tolist(),
                             ([[1, 2], [4, 5], [7, 8]]))
            self.assertEqual(splitted[1].tolist(),
                             ([[3], [6], [9]]))


    def test_sub(self):
        a = Image([1, 2, 3, 4], 2)
        b = Image([4, 3, 2, 1], 2)
        c = a - b
        self.assertEqual(c.get_matrix().tolist(),
                         [[-3, -1], [1, 3]])


    def test_isub(self):
        a = Image([1, 2, 3, 4], 2)
        b = Image([4, 3, 2, 1], 2)
        a -= b
        self.assertEqual(a.get_matrix().tolist(),
                         [[-3, -1], [1, 3]])


if __name__ == '__main__':
    main()

