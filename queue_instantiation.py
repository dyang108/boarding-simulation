from itertools import chain
from boarding_simulator import *
from random import shuffle
from collections import deque
from variables import *
from random import randint

seat_letter = ["a", "b", "c", "d", "e", "f"]

def instantiate_queue(seat_list):
    """
    Convert a list of seat numbers to a queue
    """
    return [Passenger(i, luggage_time()) for i in seat_list]

def swap_one(ordering, seen, all_seats):
    neworder = ordering[:]
    while tuple(neworder) in seen:
        a = randint(0, len(ordering) - 1)
        b = randint(0, len(ordering) - 1)
        # int(np.random.normal(loc=a, scale=3))
        # while b < 0 or b > len(ordering) - 1:
        #     b = int(np.random.normal(loc=a, scale=3))
        if all_seats[a][0] == all_seats[b][0]:
            if (all_seats[a][1] == "c" and all_seats[b][1] == "d") or (all_seats[a][1] == "c" and all_seats[b][1] == "d"):
                continue
        neworder[a], neworder[b] = neworder[b], neworder[a]
    return neworder


def seat_list(num_rows):
    y = [[None] * 6 for i in range(0, num_rows)]
    for i in range(1, num_rows + 1):
        for j in range(0, 6):
            y[i - 1][j] = (i, seat_letter[j])
    x = chain(*y)
    possible_seats = list(x)
    return possible_seats

def random_seating(num_seats):
    seat_order = range(num_seats)
    shuffle(seat_order)
    return seat_order

def block_groups(num_rows, num_groups):
    """
    Create strategy for Back to Front boarding strategy
    """
    possible_seats = [[] for i in range(num_groups)]
    max_rows_per_group = num_rows / num_groups + 1
    for i in range(1, num_rows + 1):
        for j in range(0, 6):
            possible_seats[i / max_rows_per_group].append(6 * (i - 1) + j)

    for group in possible_seats:
        shuffle(group)
    return possible_seats

def back_to_front(num_rows, num_groups):
    possible_seats = block_groups(num_rows, num_groups)
    possible_seats.reverse()
    return list(chain(*possible_seats))

def front_to_back(num_rows, num_groups):
    possible_seats = block_groups(num_rows, num_groups)
    return list(chain(*possible_seats))


# def front_to_back(num_rows, seat_per_row, num_groups):
#     """
#     Create strategy for Back to Front boarding strategy
#     """
#     max_rows_per_group = num_rows / num_groups
#     possible_seats = [list(range(k, min(num_rows + 1, k + max_rows_per_group))) * seat_per_row
#                       for k in range(1, num_rows + 1, max_rows_per_group)]
#     for group in possible_seats:
#         shuffle(group)
#     return list(chain(*possible_seats))


# def rotating_zone(num_rows, seat_per_row, num_groups):
#     """
#     Boarding Strategy: rotating back to front and front to back
#     """
#     max_rows_per_group = num_rows / num_groups
#     # groups = [[[i] * seats_per_row for i in range(k, k + max_rows_per_groups - 1)] \
#     # for k in range(1, num_rows, max_rows_per_group)]
#     # group_orders = range(num_groups, 0)
#     unordered_groups = deque([list(range(k, min(num_rows + 1, k + max_rows_per_group))) * seat_per_row
#                              for k in range(1, num_rows + 1, max_rows_per_group)])
#     groups = list()
#     # Using while True instead of while unordered_groups
#     # since we're not sure whether we're going to have an
#     # even or odd number of seats
#     while True:
#         try:
#             groups.append(unordered_groups.pop())
#             groups.append(unordered_groups.popleft())
#         except IndexError:
#             break
#     for group in groups:
#         shuffle(group)
#     return list(chain(*groups))


# def outside_in(num_rows, seat_per_row):
#     """
#     Board windows - middle - aisle seats
#     Assumption: even num seat / row . if 2 aisle. Consider creating two separate queue.
#     """

#     if seat_per_row % 2 == 0:
#         boarding_group = [list(range(1, num_rows + 1)) * 2 for _ in range(seat_per_row / 2)]
#     else:
#         #For plane ERJ145 (3 seats / row)
#         boarding_group = [list(range(1, num_rows + 1)) * 2 for _ in range(seat_per_row / 2)] + [list(range(1, num_rows + 1))]
#     for group in boarding_group:
#         shuffle(group)
#     return list(chain(*boarding_group))


# # Seats per row is across the entire row. Gotta account for that, especially for
# # the odd case.
# def reverse_pyramid(num_rows, seats_per_row, num_groups):
#     seats = num_rows * (seats_per_row / 2)

#     # A rather clunky integer ceiling function.
#     size_of_group = seats / num_groups + seats % num_groups
#     # This is for one side of the plane
#     # First case is working.
#     if seats_per_row % 2 == 0:
#         seat_order = list(range(num_rows, 0, -1)) * (seats_per_row / 2)
#         # Chunk the list into the groups, and double each of the chunks in place
#         # extend to both sides of the plane after creating the chunks just based on the one side of the plane.
#         boarding_groups = [seat_order[i:i + size_of_group] * 2 for i in range(0, len(seat_order), size_of_group)]
#     # else:
#     #     # This case isn't working. Somehow the boarding_groups is getting turned into an int.
#     #     # Start with the side of the plane with more columns
#     #     seat_order = list(range(num_rows, 0, -1)) * (seats_per_row / 2 + 1)
#     #     # Chunk it as before sorting the doubling, but only for larger side
#     #     one_side_boarding_groups = [seat_order[i:i + size_of_group] for i in range(0, len(seat_order), size_of_group)]
#     #     # Double up on one side, up to the awkward group (which we're assuming there will be)
#     #     seats_in_smaller_column = (num_rows * (seats_per_row / 2))
#     #     num_doubled_boarding_groups = seats_in_smaller_column % size_of_group # The behavior of py2's / is screwing with me
#     #     boarding_groups = [one_side_boarding_groups[i] * 2 for i in range(num_doubled_boarding_groups)]
#     #     # Add the funky split boarding group
#     #     # Gah. This code is getting janky as hell.
#     #     edge_case_seats = seats_in_smaller_column % size_of_group
#     #     boarding_groups += [one_side_boarding_groups[num_doubled_boarding_groups][:edge_case_seats + 1]] * 2
#     #     boarding_groups += one_side_boarding_groups[num_doubled_boarding_groups + 1:]
#     #     # welp, let's try that.
#     else:
#         # Specifically For the smallest plane (3 seats per row, 18 rows)
#         double_seat_order = list(range(num_rows, 0, -1)) * ((seats_per_row + 1) / 2)
#         single_seat_order = list(range(num_rows, 0, -1))
#         boarding_groups = [double_seat_order[i:i + size_of_group] + single_seat_order[i:i+ size_of_group] \
#         for i in range(0, len(double_seat_order), size_of_group)]

#     # Shuffle each of the chunks
#     shuffle_groups(boarding_groups)

#     return list(chain(*boarding_groups))
#     # return boarding_groups


# def staggered_reverse_pyramid(num_rows, seats_per_row):
#     pass


# def block_boarding(num_rows, seats_per_row):
#     pass


# def shuffle_groups(boarding_groups):
#     for group in boarding_groups:
#         shuffle(group)


if __name__ == '__main__':
    queue = reverse_pyramid(18, 3, 5)
    print(queue)
    #assert len(queue) == 10 * 3
