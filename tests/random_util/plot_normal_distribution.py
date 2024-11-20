# file: plot_normal_distribution.py

import math
import matplotlib.pyplot as plt
from common_util.random_util.random_number import RandomNumberGenerator

# entry: [ <mean>, <standard_deviation> ]
plot_cases = [
    [ 0.0, 10.0 ],
    [ 0.0, 20.0 ],
    [ 0.0, 50.0 ],
    [ 100.0, 10.0 ],
    [ 200.0, 10.0 ],
    [ -50.0, 20.0 ],
    [ -150.0, 20.0 ],
    [ 100.0, 50.0 ],
    [ -100.0, 100.0 ],
]

def main():
    array_size = 500
    array_mid_point = array_size // 2
    x_array = [i - array_mid_point for i in range(array_size)]
    for mean, standard_deviation in plot_cases:
        y_array = [0] * array_size
        for _ in range(50000):
            value = RandomNumberGenerator.normal_distribution(mean, standard_deviation)
            index = math.floor(value) + array_mid_point
            if index >= 0 and index < array_size:
                y_array[index] += 1
        plt.plot(x_array, y_array)
    plt.title('Normal Distribution')
    plt.xlabel('x')
    plt.ylabel('normal_distribution(x)')
    plt.show()
    return

if __name__ == '__main__':
    main()

# --- end of file --- #
