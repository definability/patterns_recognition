class MatrixPointer:


    def __init__(self, data, size=None, offset=(0,0)):
        """Create a matrix pointer.

        Keyword arguments:
        data -- array, matrix of matrix pointer;
        size -- tuple (width, height) with size of current image fragment;
            default is None, but you can use it only when data is a matrix;
        offset -- tuple (x, y) with offset of current image fragment
            from the left top element of the matrix; default is (0, 0).
        """

        if size is None:
            if type(data) is not list or type(data[0]) is not list:
                raise ValueError('If size is not set, data should be a matrix')
            size = (len(data[0]), len(data))

        if isinstance(data, MatrixPointer):
            self.__data = data.get_data()
            self.__original_size = data.get_size()
            self.__size = size
            self.__offset = data.get_offset(offset)
        else:
            self.__data = self.__flatten(data)
            self.__original_size = size
            self.__size = size
            self.__offset = offset


    def __flatten(self, lst):
        """Convert lst to one-dimensional list.
        
        Works with non-lists, lists and matrices.
        """
        if type(lst) is not list:
            return [lst]
        elif type(lst[0]) is not list:
            return lst
        return sum(lst, [])


    def get_data(self, source=False):
        """Get list with data, current pointer points to.
        
        Keyword arguments:
        source -- whether you need the source data (True),
            or cropped fragment (False); default is False.
        """
        if source:
            return self.__data
        return [e for e in self.get_generator()]


    def get_generator(self):
        """Get generator of list with data, current pointer points to."""
        result = []
        for y in range(self.__offset[1], self.__offset[1]+self.__size[1]):
            for e in self.__data[self.__original_size[0]*y+self.__offset[0]:
                                 self.__original_size[0]*y+self.__offset[0]
                                 +self.__size[0]]:
                yield e


    def get_offset(self, initial_offset=(0,0), y=0):
        """Get current pointer offset and add new offset to it.
        
        Useful for the case, when you create new pointer
        on the basis of existing one.

        Keyword arguments:
        initial_offset -- tuple (x, y) with offset from current pointer's
            left upper corner either horizontal offset;
        y -- vertical offset, if `initial_offset` is a horizontal offset.
        """

        if type(initial_offset) is tuple:
            return (self.__offset[0]+initial_offset[0],
                    self.__offset[1]+initial_offset[1])

        return (self.__offset[0]+initial_offset,
                self.__offset[1]+y)


    def get_size(self):
        """Get width and height of current matrix"""
        return self.__size


    def split_vertical(self, width):
        """Split the matrix vertically.

        Get two pointers:
        - to first `width` columns of the matrix;
        - to other columns of the matrix.
        """
        left = MatrixPointer(self, (width, self.__size[1]), self.get_offset())
        right = MatrixPointer(self, (self.__size[0]-width, self.__size[1]),
                                     self.get_offset(width, 0))
        return (left, right)


    def split_horizontal(self, height):
        """Split the matrix horizontally.

        Get two pointers:
        - to first `height` rows of the matrix;
        - to other rows of the matrix.
        """
        top = MatrixPointer(self, (self.__size[0], height), self.get_offset())
        bottom = MatrixPointer(self, (self.__size[0], self.__size[1]-height),
                                     self.get_offset(0, height))
        return (top, bottom)


    def __sync_generators(self, *matrices):
        """Create synchronized generator based on length of current matrix.

        Positional arguments:
        matrices -- matrices,
            which are needed to be iterated during the operation.
        """
        generators = [m.get_generator() for m in matrices]
        for v in self.get_generator():
            yield [v]+[g.next() for g in generators]


    def map(self, f, *matrices):
        """Apply function to matrices and return list with processed values.
        
        Keyword arguments:
        f -- function to apply;

        Positional arguments:
        matrices -- matrices,
            which are needed to be iterated during the operation.
        """
        result = []
        for v in self.__sync_generators(*matrices):
            result.append(f(*v))
        return result


    def reduce(self, f, initial_value=None, *matrices):
        """Apply function to matrices using accumulator and return the result.

        Keyword arguments:
        f -- function to apply;

        Positional arguments:
        matrices -- matrices,
            which are needed to be iterated during the operation.
        """
        result = initial_value
        b = self.get_generator()
        for v in self.__sync_generators(*matrices):
            result = (f(result, *v))
        return result


    def __sub__(self, matrix):
        return self.map(lambda x, y: x-y, matrix)

