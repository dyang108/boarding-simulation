from boarding_simulator import *
from queue_instantiation import *
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from random import randrange
from variables import *

def run_simulation(all_seats, seat_order, num_rows, verbose=False):
    # Create a plane
    plane = instantiate_plane(num_rows)
    queue = instantiate_queue([all_seats[ind] for ind in seat_order])
    return float(simulation(queue, plane, verbose))

def run_mcmc(num_rows, seating_method):
    seen = set()
    all_seats = seat_list(num_rows)
    curr_seating_arrangement = seating_method(len(all_seats))
    curr_best_arr = curr_seating_arrangement
    curr_best = float("inf")
    # curr_best = 0
    same_result_repeated = 0

    while same_result_repeated < min_repeats:
        curr_seating_arrangement = swap_one(curr_best_arr, seen, all_seats)
        seen.add(tuple(curr_seating_arrangement))
        boarding_time = run_simulation(all_seats, curr_seating_arrangement, num_rows)
        if boarding_time < curr_best:
            same_result_repeated = 0
            curr_best = boarding_time
            print curr_best
            curr_best_arr = curr_seating_arrangement
        else:
            same_result_repeated += 1
    blah = input('Enter something: ')
    run_simulation(all_seats, curr_best_arr, num_rows, True)
    print [all_seats[ind] for ind in curr_best_arr]
    return curr_best

def run_grouped(num_rows, num_groups, seating_method):
    all_seats = seat_list(num_rows)

    curr_seating_arrangement = seating_method(num_rows, num_groups)
    boarding_time = run_simulation(all_seats, curr_seating_arrangement, num_rows)

    return boarding_time

# default seats per row = 6
if __name__ == '__main__':
    num_groups = 3
    random_plane_result = run_mcmc(num_rows, random_seating)
    back_to_front_result = run_grouped(num_rows, num_groups, back_to_front)
    front_to_back_result = run_grouped(num_rows, num_groups, front_to_back)
    print "random_plane_result " + str(random_plane_result)
    print "back_to_front_result " + str(back_to_front_result)
    print "front_to_back_result " + str(front_to_back_result)

# def graph(results_list, title):
#     # Set up graph of results
#     bar_width = 0.35
#     index = np.arange(len(results_list))
#     graph = plt.bar(index, results_list, bar_width)
#     # plt.xlabel('')
#     plt.ylabel('Time Steps')
#     plt.title(title + ' : Boarding Time for Different Strategies')
#     plt.xticks(index + bar_width, strategy_name)
#     locs, labels = plt.xticks()
#     plt.setp(labels, rotation=45)
#     plt.gcf().subplots_adjust(bottom=0.25)
#     plt.show()
