# file: random_array.py

class RandomArray:

    @staticmethod
    def random_list(count, random_function):
        '''
        Generate a list of random values

        :param count: the number of random values
        :param random_function: the function use to generate the random values
        :type count: int
        :type random_function: function

        :return: a list of random values
        :rtype: list
        '''
        return [random_function() for _ in range(count)]
    
    @staticmethod
    def random_matrix(row, column, random_function):
        '''
        Generate a matrix of random values

        :param row: number of row of the matrix
        :param column: number of column of the matrix
        :param random_function: the function use to generate the random values
        :type row: int
        :type column: int
        :type random_function: function

        :return: a row x column matrix of random values
        :rtype: matrix (row x column)
        '''
        result = []
        for _ in range(row):
            result.append(RandomArray.random_list(column, random_function))
        return result
    
    @staticmethod
    def random_array(shape, random_function):
        '''
        Generate an array of random values

        :param shape: the dimensions of the array
        :param random_function: the function use to generate the random values
        :type shape: tuple of int
        :type random_function: function

        :return: an array of random values
        :rtype: array
        '''
        if len(shape) < 1:
            raise ValueError(f'invalid shape: {shape}')
        if len(shape) == 1:
            return RandomArray.random_list(shape[0], random_function)
        result = []
        for _ in range(shape[0]):
            result.append(RandomArray.random_array(shape[1:], random_function))
        return result

# --- end of file --- #
