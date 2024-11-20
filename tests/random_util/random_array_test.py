# file: random_array_test.py

import unittest
import random
import numpy as np
from common_util.random_util.random_array import RandomArray

class RandomNumberArrayTest(unittest.TestCase):

    def setUp(self):
        # random.seed(42)
        return super().setUp()

    def test_01(self):
        for i in range(20):
            r_list = RandomArray.random_list(5, lambda: random.randint(0, 5))
            print(r_list)
            print()
        return
    
    def test_02(self):
        for i in range(20):
            r_list = RandomArray.random_list(5, lambda: random.uniform(-0.5, 0.5))
            print(r_list)
            print()
        return
    
    def test_03(self):
        for i in range(20):
            r_matrix = RandomArray.random_matrix(5, 6, lambda: random.randint(0, 5))
            print(r_matrix)
            print()
        return
    
    def test_04(self):
        shape = [3, 5, 6]
        for i in range(20):
            r_array = RandomArray.random_array(shape, lambda: random.randint(0, 5))
            for element in r_array:
                print(element)
            np_array = np.array(r_array)
            print(f'np array shape: {np_array.shape}')
            print()
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
