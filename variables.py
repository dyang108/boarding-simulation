# Author: Derick Yang
import numpy as np
# number of ticks to move sideways one seat
side_move_ticks = 2
use_constants = True

# how many "moves" it takes to seat under these scenarios
# my hypothesis: 0 3 4 5
no_block = 0
def c_block_b():
    if use_constants:
        return 3
    else:
        return int(np.random.normal(loc=3.0, scale=1))
def b_block_a():
    if use_constants:
        return 4
    else:
        return int(np.random.normal(loc=4.0, scale=1))
def bc_block_a():
    if use_constants:
        return 5
    else:
        return int(np.random.normal(loc=3.0, scale=1.5))

const_num_rows = 23 # keep this constant

min_repeats = 1000

simulation_time_step = .05

num_start_points = 1

# parameter for exponential distribution of group sizes
group_lambd = 0.5

num_groups = 3


# Silly constant function for now, but will
# allow us to easily create a new luggage_time
# function that has a random distribution to it.
def luggage_time():
    # constant time
    if use_constants:
        return 10
    # uniform random 0-20
    # return randrange(1, 21)
    # normal distribution around 10
    else:
        return int(np.random.normal(loc=7.0, scale=3))

