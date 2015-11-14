class MatrixPointer:


    def __init__(self, data, size=None, offset=(0,0), transpose=False):
        """Create a matrix pointer.

        Keyword arguments:
        data -- array, matrix of matrix pointer;
        size -- tuple (width, height) with size of current image fragment;
            default is None, but you can use it only when data is a matrix;
        offset -- tuple (x, y) with offset of current image fragment
            from the left top element of the matrix; default is (0, 0);
        transpose -- True if matrix needs to be transposed and False otherwise;
            default is False.
        """


        if size is None:
            if type(data) is not list or type(data[0]) is not list:
                raise ValueError('If size is not set, data should be a matrix')
            if not transpose:
                size = (len(data[0]), len(data))
            else:
                size = (len(data), len(data[0]))

        if isinstance(data, MatrixPointer):
            self.__data = data.get_data(True)
            self.__original_size = data.get_size(True)
            self.__size = size
            self.__offset = data.get_offset(offset)
        else:
            self.__data = self.__flatten(data)
            self.__original_size = size
            self.__size = size
            self.__offset = offset
            if transpose:
                self.__transpose()


    def __flatten(self, lst):
        """Convert lst to one-dimensional list.
        
        Works with non-lists, lists and matrices.
        """
        if type(lst) is not list:
            return [lst]
        elif type(lst[0]) is not list:
            return lst
        return sum(lst, [])


    def __transpose(self):
        """Transpose the matrix."""
        self.__data = [d for i in range(self.__original_size[1])
                         for d in self.__data[i:len(self.__data):
                                              self.__original_size[1]]]


    def get_data(self, source=False):
        """Get list with data, current pointer points to.
        
        Keyword arguments:
        source -- whether you need the source data (True),
            or cropped fragment (False); default is False.
        """
        if source:
            return self.__data
        if self.__size == (0, 0):
            return None
        return [e for e in self.get_generator()]


    def get_generator(self):
        """Get generator of list with data, current pointer points to."""
        if self.__size == (0, 0):
            return
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


    def get_size(self, original=False):
        """Get width and height of current matrix"""
        return self.__original_size if original else self.__size


    def split_vertical(self, width):
        """Split the matrix vertically.

        Get two pointers:
        - to first `width` columns of the matrix;
        - to other columns of the matrix.
        """
        height = 0 if width == 0 else self.__size[1]
        left = MatrixPointer(self, (width, height))
        height = 0 if width == self.__size[0] else self.__size[1]
        right = MatrixPointer(self, (self.__size[0]-width, height),
                                     (width, 0))
        return (left, right)


    def split_horizontal(self, height):
        """Split the matrix horizontally.

        Get two pointers:
        - to first `height` rows of the matrix;
        - to other rows of the matrix.
        """
        width = 0 if height == 0 else self.__size[0]
        top = MatrixPointer(self, (width, height))
        width = 0 if height == self.__size[1] else self.__size[0]
        bottom = MatrixPointer(self, (width, self.__size[1]-height),
                                     (0, height))
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
        return [f(*v) for v in self.__sync_generators(*matrices)]


    def reduce(self, f, current_value=None, *matrices):
        """Apply function to matrices using accumulator and return the result.

        Keyword arguments:
        f -- function to apply;

        Positional arguments:
        current_value -- initial value,
            which will be passed to f in the first operation.
        matrices -- matrices,
            which are needed to be iterated during the operation.
        """
        b = self.get_generator()
        for v in self.__sync_generators(*matrices):
            current_value = (f(current_value, *v))
        return current_value

