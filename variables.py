import numpy as np
# number of ticks to move sideways one seat
side_move_ticks = 2
# how many "moves" it takes to seat under these scenarios
# my hypothesis: 0 3 4 5
no_block = 0
c_block_b = 3
b_block_a = 4
bc_block_a = 5

num_rows = 10

min_repeats = 50

simulation_time_step = .25

# Silly constant function for now, but will
# allow us to easily create a new luggage_time
# function that has a random distribution to it.
def luggage_time():
    # constant time
    return 10
    # uniform random 0-20
    # return randrange(1, 21)
    # normal distribution around 10
    # return int(np.random.normal(loc=5.0, scale=1))

