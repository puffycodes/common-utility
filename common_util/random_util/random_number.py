# file: random_number.py

# Normal Distribution
# Ref: https://en.wikipedia.org/wiki/Normal_distribution
#
# Generation Values for Normal Distribution
# Ref: https://en.wikipedia.org/wiki/Normal_distribution#Generating_values_from_normal_distribution

import random

class RandomNumberGenerator:

    @staticmethod
    def normal_distribution(mean=0.0, standard_deviation=1.0):
        '''
        Generate a random value from a normal distribution.

        :param mean: the mean of the normal distribution
        :param standard_deviation: the standard deviation of the normal distribution
        :type mean: float, optional
        :type standard_deviation: float, optional

        :return: the random value
        :rtype: float
        '''
        random_number = RandomNumberGenerator.normal_distribution_base()
        random_number = random_number * standard_deviation + mean
        return random_number
    
    @staticmethod
    def normal_distribution_base():
        '''
        Generate a random value from a normal distribution with mean 0.0 and standard deviation 1.0.

        :meta private:

        :return: the random value
        :rtype: float
        '''
        sum = 0.0
        for _ in range(12):
            sum += random.uniform(0.0, 1.0)
        sum -= 6.0
        return sum

# --- end of file --- #
