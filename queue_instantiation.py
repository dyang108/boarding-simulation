# author: Derick Yang & Tanner Stirrat
from itertools import chain
from boarding_simulator import *
from random import shuffle
from collections import deque
from variables import *
from random import randint
from random import expovariate

seat_letter = ["a", "b", "c", "d", "e", "f"]
seat_ranks = {
    "a": 1,
    "f": 1,
    "b": 2,
    "e": 2,
    "c": 3,
    "d": 3    
}

def instantiate_queue(seat_list):
    """
    Convert a list of seat numbers to a queue
    """
    return [Passenger(i, luggage_time()) for i in seat_list]

def swap_one(ordering, seen, all_seats):
    """
    The swapping function used to approach the optimal solution. For each iteration, this function is called once.
    """
    neworder = ordering[:]
    p = randint(0, 10)
    while tuple(neworder) in seen:
        if p < 6:
            a = randint(0, len(ordering) - 1)
            b = randint(0, len(ordering) - 1)
            if all_seats[a][0] == all_seats[b][0]:
                if (all_seats[a][1] == "c" and all_seats[b][1] == "d") or (all_seats[a][1] == "c" and all_seats[b][1] == "d"):
                    continue
            neworder[a], neworder[b] = neworder[b], neworder[a]
        else:
            a = randint(0, len(ordering) - 1)
            b = randint(0, len(ordering) - 1)
            c = randint(0, len(ordering) - 1)
            if a == b or b == c or a == c:
                continue
            neworder[a], neworder[b], neworder[c] = neworder[c], neworder[a], neworder[b]
    return neworder

def swap_parties(ordering, seen):
    neworder = ordering[:]
    while tuple(neworder) in seen:
        a = randint(0, len(ordering) - 1)
        b = randint(0, len(ordering) - 1)
        neworder[a], neworder[b] = neworder[b], neworder[a]
    return neworder

def seat_list(num_rows):
    """
    returns the list of seats with the given configuration of plane
    """
    y = [[None] * 6 for i in range(0, num_rows)]
    for i in range(1, num_rows + 1):
        for j in range(0, 6):
            y[i - 1][j] = (i, seat_letter[j])
    x = chain(*y)
    possible_seats = list(x)
    return possible_seats

def random_seating(num_seats):
    """
    A random seat order
    """
    seat_order = range(num_seats)
    shuffle(seat_order)
    return seat_order

def random_seating_with_parties(num_seats):
    """
    Think families and groups of people, exponentially distributed in size
    """
    group_order = []
    i = 0
    while i < num_seats:
        r = int(expovariate(group_lambd) + 1)
        if i + r > num_seats:
            continue

        new_party = []
        for j in range(r):
            new_party.append(i)
            i += 1
        shuffle(new_party)
        group_order.append(new_party)

    shuffle(group_order)
    return group_order

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

# the most typical configuration
def back_to_front(num_rows, num_groups):
    possible_seats = block_groups(num_rows, num_groups)
    possible_seats.reverse()
    return list(chain(*possible_seats))

def front_to_back(num_rows, num_groups):
    possible_seats = block_groups(num_rows, num_groups)
    return list(chain(*possible_seats))

# proposed optimal configuration
# author: Zach Finn
def window_middle_aisle(num_seats):
    num_rows = num_seats / 6
    order = []
    a = 0
    b = 1
    c = 2
    d = 3
    e = 4
    f = 5
    window_left = []
    window_right = []
    middle_left = []
    middle_right = []
    aisle_left = []
    aisle_right = []
    for i in range(num_rows):
        window_left.append(a)
        window_right.append(f)
        middle_left.append(b)
        middle_right.append(e)
        aisle_left.append(c)
        aisle_right.append(d)
        a = a+6
        b = b+6
        c = c+6
        d = d+6
        e = e+6
        f = f+6

    window_left.reverse()
    window_right.reverse()
    middle_left.reverse()
    middle_right.reverse()
    aisle_left.reverse()
    aisle_right.reverse()

    for i in range(num_rows):
        order.append(window_left[i])
    for i in range(num_rows):
        order.append(window_right[i])
    for i in range(num_rows):
        order.append(middle_left[i])
    for i in range(num_rows):
        order.append(middle_right[i])
    for i in range(num_rows):
        order.append(aisle_left[i])
    for i in range(num_rows):
        order.append(aisle_right[i])
    return order

# author: Zach Finn
def worst(num_seats):
    num_rows = num_seats / 6
    order = []
    a = 0
    b = 1
    c = 2
    d = 3
    e = 4
    f = 5
    window_left = []
    window_right = []
    middle_left = []
    middle_right = []
    aisle_left = []
    aisle_right = []
    for i in range(num_rows):
        window_left.append(a)
        window_right.append(f)
        middle_left.append(b)
        middle_right.append(e)
        aisle_left.append(c)
        aisle_right.append(d)
        a = a+6
        b = b+6
        c = c+6
        d = d+6
        e = e+6
        f = f+6

    for i in range(num_rows):
        order.append(aisle_left[i])
        order.append(middle_left[i])
        order.append(window_left[i])
        order.append(aisle_right[i])
        order.append(middle_right[i])
        order.append(window_right[i])

    return order

def optimality_ratio(c):
    count = len(c)
    s = 0
    for i in range(0, count / 3):
        if c[i][1] == "a" or c[i][1] == "f":
            s += 1
    return float(s) / (count / 3)
