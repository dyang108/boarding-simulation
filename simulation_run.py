from boarding_simulator import *
from queue_instantiation import *
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from random import randrange


# Plane ERJ145
# 18 rows +  3 seats / row + 1 aisles


# Plane Boeing 747-400
# 29 rows +  8 seats / row + 2 aisles


# Plane Boeing 737-900
# 27 rows +  6 seats / row b+ 1 aisles

# Number of trials
sample_size = 100


# These are lists of functions, imported from the other module
strategies_with_groups = [back_to_front, front_to_back, rotating_zone, reverse_pyramid]
strategies_without_groups = [random_seat, outside_in]

# Names of the strategies.
strategy_name = ["Random Boarding",
                 "Outside In",
                 "Back to Front",
                 "Front to Back",
                 "Rotating Zone",
                 "Reverse Pyramid"]


def run_simulation(boarding_strategy,
                   sample_size,
                   luggage_time, num_rows,
                   seat_per_row, num_groups=False):
    """
    boarding_strategy: a function to create different boarding strategy,
    imported from the queue_instantiation module.
    """
    time_steps = 0
    for i in range(sample_size):
        # Create a plane
        plane = instantiate_plane(num_rows)
        # Two different approaches depending on whether
        # there's 
        if num_groups:
            order_seats = boarding_strategy(num_rows,
                                            seat_per_row,
                                            num_groups)
        else:
            order_seats = boarding_strategy(num_rows, seat_per_row)
        queue = instantiate_queue(order_seats, luggage_time())
        time_steps += simulation(queue, plane)
    return time_steps / float(sample_size)


# Run simulation for small plane

def simulation_plane(num_rows, seat_per_row, num_groups):
    result_no_groups = [run_simulation(strategies_without_groups[i], sample_size,
                                       luggage_time, num_rows,
                                       seat_per_row)
                        for i in range(len(strategies_without_groups))]
    # Chosen num_groups = 5 (can be optimized)
    result_with_groups = [run_simulation(strategies_with_groups[i], sample_size,
                                         luggage_time, num_rows,
                                         seat_per_row, num_groups)
                          for i in range(len(strategies_with_groups))]
    result = result_no_groups + result_with_groups
    return result


def graph(results_list, title):
    # Set up graph of results
    bar_width = 0.35
    index = np.arange(len(results_list))
    graph = plt.bar(index, results_list, bar_width)
    # plt.xlabel('')
    plt.ylabel('Time Steps')
    plt.title(title + ' : Boarding Time for Different Strategies')
    plt.xticks(index + bar_width, strategy_name)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45)
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.show()

# Silly constant function for now, but will
# allow us to easily create a new luggage_time
# function that has a random distribution to it.
def luggage_time():
    # constant time
    return 10
    # uniform random 0-20
    # return randrange(1, 21)
    # normal distribution around 10
    # return int(np.random.normal(loc=10.0, scale=5))


if __name__ == '__main__':
    num_groups = 3
    small_plane = simulation_plane(18, 3, num_groups)
    medium_plane = simulation_plane(27, 6, num_groups)
    large_plane = simulation_plane(29, 4, num_groups)

    print(small_plane)
    print(medium_plane)
    print(large_plane)

    # constant luggage time: 10
    # graph([248.83, 239.26, 302.59, 419.5, 280.53, 220.76], "Small Plane")
    # graph([621.48, 613.88, 905.78, 1076.28, 861.16, 627.8], "Medium Plane")
    # graph([452.38, 442.7, 600.51, 764.9, 557.21, 432.39], "Big Plane")

    # uniform random luggage time: 0-20
    # graph([240.85, 271.34, 311.7, 417.27, 303.38, 219.03], "Small Plane")
    # graph([793.81, 771.33, 1153.53, 1452.21, 1160.64, 819.34], "Medium Plane")
    # graph([439.58, 427.1, 530.16, 726.2, 556.41, 430.83], "Big Plane")
