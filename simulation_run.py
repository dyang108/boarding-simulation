# author: Derick Yang & Tanner Stirrat
from boarding_simulator import *
from queue_instantiation import *
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from random import randrange
from variables import *
from itertools import chain

def run_simulation(all_seats, seat_order, num_rows, verbose=False):
    # Create a plane
    plane = instantiate_plane(num_rows)
    queue = instantiate_queue([all_seats[ind] for ind in seat_order])
    return float(simulation(queue, plane, verbose))

def run_mcmc(num_rows, seating_method):
    all_seats = seat_list(num_rows)
    (opt_config, t) = optimize_config(seating_method(len(all_seats)), all_seats, num_rows)
    
    for i in range(num_start_points - 1):
        (config, new_t) = optimize_config(seating_method(len(all_seats)), all_seats, num_rows)
        if new_t < t:
            t = new_t
            opt_config = config

    # blah = input('Enter something: ')
    # run_simulation(all_seats, opt_config, num_rows, True)
    conf = [all_seats[ind] for ind in opt_config]
    return t, optimality_ratio(conf)

def optimize_config(curr_seating_arrangement, all_seats, num_rows):
    seen = set()
    curr_best_arr = curr_seating_arrangement

    curr_best = float("inf")
    same_result_repeated = 0

    while same_result_repeated < min_repeats:
        curr_seating_arrangement = swap_one(curr_best_arr, seen, all_seats)
        seen.add(tuple(curr_seating_arrangement))
        boarding_time = run_simulation(all_seats, curr_seating_arrangement, num_rows)
        if boarding_time < curr_best:
            same_result_repeated = 0
            curr_best = boarding_time
            curr_best_arr = curr_seating_arrangement
        elif boarding_time == curr_best:
            curr_best_arr = curr_seating_arrangement
            same_result_repeated += 1
        else:
            same_result_repeated += 1
    return (curr_best_arr, boarding_time)

def run_parties(num_rows):
    seen = set()
    all_seats = seat_list(num_rows)
    parties = random_seating_with_parties(len(all_seats))
    curr_party_arrangement = range(len(parties))
    best_time = float("inf")
    same_result_repeated = 0

    while same_result_repeated < min_repeats:
        curr_party_arrangement = swap_parties(curr_party_arrangement, seen)
        seen.add(tuple(curr_party_arrangement))
        boarding_time = run_simulation(all_seats, chain(*[parties[i] for i in curr_party_arrangement]), num_rows)
        if boarding_time < best_time:
            same_result_repeated = 0
            best_time = boarding_time
            curr_best_arrangement = curr_party_arrangement
        else:
            same_result_repeated += 1
    blah = input('Enter something: ')
    opt_config = chain(*[parties[i] for i in curr_party_arrangement])
    run_simulation(all_seats, opt_config, num_rows, True)
    return best_time

def run_individual(num_rows, seating_method, verbose=False):
    all_seats = seat_list(num_rows)
    curr_seating_arrangement = seating_method(len(all_seats))

    boarding_time = run_simulation(all_seats, curr_seating_arrangement, num_rows, verbose)
    return boarding_time

def run_grouped(num_rows, num_groups, seating_method, verbose=False):
    all_seats = seat_list(num_rows)

    curr_seating_arrangement = seating_method(num_rows, num_groups)
    boarding_time = run_simulation(all_seats, curr_seating_arrangement, num_rows, verbose)

    return boarding_time

def exp1():
    use_constants = True
    random_plane_result, opt = run_mcmc(const_num_rows, random_seating)
    return random_plane_result

def exp2():
    use_constants = False
    random_plane_result, opt = run_mcmc(const_num_rows, random_seating)
    return random_plane_result

def exp3():
    use_constants = True
    back_to_front_result = run_grouped(const_num_rows, num_groups, back_to_front)
    return back_to_front_result

def exp4():
    use_constants = True
    front_to_back_result = run_grouped(const_num_rows, num_groups, front_to_back)
    return front_to_back_result

def exp5():
    use_constants = True
    # save each of the boarding times in each iteration of mcmc, since we cannot do better
    run_mcmc(const_num_rows, window_middle_aisle)

def exp6():
    use_constants = True
    return run_parties(const_num_rows)

def sensitivity(method):
    for i in range(1, 25):
        for j in range(1, 10):
            if i / j  < 1:
                continue
            s = 0
            for c in range(0, 50):
                result = run_grouped(i, j, method)
                s += result
            print str(i) + ", " + str(j) + ", " + str(s/50)

# default seats per row = 6
if __name__ == '__main__':
    print exp1()
    print exp2()
    print exp3()
    print exp4()
    exp5()
    print exp6()
    sensitivity(front_to_back)
    sensitivity(back_to_front)
