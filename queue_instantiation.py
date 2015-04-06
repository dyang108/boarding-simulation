from itertools import chain
from boarding_simulator import *
from random import shuffle
from collections import deque

# Thao: Haven't tested codes yet


def instantiate_queue(seat_list, luggage_time):
    """
    Convert a list of seat numbers to a queue
    """
    return [Passenger(i, luggage_time) for i in seatList]


def random_seat(seat_per_row, num_rows):
    possible_seats = list(chain([[i] * seats_per_row
                          for i in range(1, num_rows + 1)]))
    return shuffle(possible_seats)


def back_to_front(num_rows, seat_per_row, num_groups):
    """
    Create strategy for Back to Front boarding strategy
    """
    max_rows_per_group = num_rows / num_groups
    possible_seats = [[[i] * seats_per_row
                      for i in range(k, min(num_rows + 1, k + max_rows_per_groups))]
                      for k in range(1, num_rows + 1, max_rows_per_group)]
    possible_seats = [shuffle(group) for group in possible_seats]
    possible_seats.reverse()
    return list(chain(possible_seats))


def front_to_back(num_rows, seat_per_row, num_groups):
    """
    Create strategy for Back to Front boarding strategy
    """
    max_rows_per_group = num_rows / num_groups
    possible_seats = [[[i] * seats_per_row for i in range(k, min(num_rows + 1, k + max_rows_per_groups))]
                      for k in range(1, num_rows + 1, max_rows_per_group)]
    possible_seats = [shuffle(group) for group in possible_seats]
    return list(chain(possible_seats))


def rotating_zone(num_rows, seat_per_row, num_groups):
    """
    Boarding Strategy: rotating back to front and front to back
    """
    max_rows_per_group = num_rows / num_groups
    # groups = [[[i] * seats_per_row for i in range(k, k + max_rows_per_groups - 1)] \
    # for k in range(1, num_rows, max_rows_per_group)]
    # group_orders = range(num_groups, 0)
    unordered_groups = deque([[[i] * seats_per_row for i in range(k, min(num_rows + 1, k + max_rows_per_groups))]
                             for k in range(1, num_rows + 1, max_rows_per_group)])
    groups = deque()
    while True:
        try:
            groups.append(unordered_groups.pop())
            groups.append(unordered_groups.popleft())
        except IndexError:
            break
    groups = [shuffle(group) for group in groups]
    return list(chain(groups))


def outside_in(num_rows, seat_per_row):
    """
    Board windows - middle - aisle seats
    Assumption: even num seat / row , 1 aisle -> What about 2?
    """
    boarding_group = [[i] * 2 for range(1, num_rows + 1)] for _ in range()
    boarding_group = 
    # not finished
