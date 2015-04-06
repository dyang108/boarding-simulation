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
    possible_seats = list(chain(*[[i] * seat_per_row
                          for i in range(1, num_rows + 1)]))
    shuffle(possible_seats)
    return possible_seats


def back_to_front(num_rows, seat_per_row, num_groups):
    """
    Create strategy for Back to Front boarding strategy
    """
    max_rows_per_group = num_rows / num_groups
    possible_seats = [list(range(k, min(num_rows + 1, k + max_rows_per_group))) * seat_per_row \
                            for k in range(1, num_rows + 1, max_rows_per_group)]
    for group in possible_seats:
        shuffle(group)
    possible_seats.reverse()
    return list(chain(*possible_seats))


def front_to_back(num_rows, seat_per_row, num_groups):
    """
    Create strategy for Back to Front boarding strategy
    """
    max_rows_per_group = num_rows / num_groups
    possible_seats = [list(range(k, min(num_rows + 1, k + max_rows_per_group))) * seat_per_row \
                            for k in range(1, num_rows + 1, max_rows_per_group)]
    for group in possible_seats:
        shuffle(group)
    return list(chain(*possible_seats))


def rotating_zone(num_rows, seat_per_row, num_groups):
    """
    Boarding Strategy: rotating back to front and front to back
    """
    max_rows_per_group = num_rows / num_groups
    # groups = [[[i] * seats_per_row for i in range(k, k + max_rows_per_groups - 1)] \
    # for k in range(1, num_rows, max_rows_per_group)]
    # group_orders = range(num_groups, 0)
    unordered_groups = deque([list(range(k, min(num_rows + 1, k + max_rows_per_group))) * seat_per_row \
                            for k in range(1, num_rows + 1, max_rows_per_group)])
    groups = list()
    while True:
        try:
            groups.append(unordered_groups.pop())
            groups.append(unordered_groups.popleft())
        except IndexError:
            break
    for group in groups:
        shuffle(group)
    return list(chain(*groups))


def outside_in(num_rows, seat_per_row):
    """
    Board windows - middle - aisle seats
    Assumption: even num seat / row . if 2 aisle. Consider creating two separate queue.
    """

    if seat_per_row % 2 == 0:
        boarding_group = [list(range(1, num_rows + 1)) * 2 for _ in range(seat_per_row / 2)]
    else:
        #For plane ERJ145 (3 seats / row)
        boarding_group = [list(range(1, num_rows + 1)) * 2 for _ in range(seat_per_row / 2)] + [list(range(1, num_rows + 1))]
    for group in boarding_group:
        shuffle(group)
    return list(chain(*boarding_group))


if __name__ == '__main__':
    pass


    
