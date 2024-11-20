# file: random_number_test.py

import unittest
import math
from common_util.random_util.random_number import RandomNumberGenerator
from common_util.random_util.random_array import RandomArray

class RandomNumberGeneratorTest(unittest.TestCase):

    def test_normal_distribution_01a(self):
        for _ in range(20):
            value = RandomNumberGenerator.normal_distribution_base()
            print(value)
        print()
        return
    
    def test_normal_distribution_01b(self):
        value_list = RandomArray.random_list(20, RandomNumberGenerator.normal_distribution_base)
        for value in value_list:
            print(value)
        print()
        return
    
    def test_normai_distribution_02(self):
        zone_unit = 20
        zone_count = 8
        array_size = zone_count * zone_unit
        array_mid_point = (zone_count // 2) * zone_unit
        count = [0] * array_size
        for _ in range(5000):
            value = RandomNumberGenerator.normal_distribution(array_mid_point, zone_unit)
            index = math.floor(value)
            if index < 0:
                index = 0
            if index >= array_size:
                index = array_size - 1
            count[index] += 1
        for i in range(zone_count):
            print(count[i*zone_unit:(i+1)*zone_unit])
        print()
        return

    def test_normal_distribution_03(self):
        # intervals in term of distance from mean (unit: sigma):
        #      [ (-inf,-3), (-3,-2), (-2,-1), (-1,0), (0,1), (1,2), (2,3), (3,inf) ]
        probabilities_normal_distribution = [ 0.001, 0.021, 0.136, 0.341, 0.341, 0.136, 0.021, 0.001 ]
        total = 10000
        sectors = 8
        mid_point = 8 // 2
        count = [0] * 8
        for _ in range(total):
            value = RandomNumberGenerator.normal_distribution_base()
            index = math.floor(value) + mid_point
            if index < 0:
                index = 0
            if index >= sectors:
                index = sectors - 1
            count[index] += 1
        print()
        for i in range(sectors):
            probability = count[i] / total
            diff = probability - probabilities_normal_distribution[i]
            print(
                f'{i}: {probability:.3f} ({probabilities_normal_distribution[i]:.3f})'
                f' {diff:+.3f}'
            )
        print()
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
