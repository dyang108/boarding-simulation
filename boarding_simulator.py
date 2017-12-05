import time
from variables import *

class Row(object):
    """Represents one row of the airplane"""
    def __init__(self, number):
        self.next_row = None
        self.aisle_occupied = None
        self.seats_occupied = {
            "a": None,
            "b": None,
            "c": None,
            "d": None,
            "e": None,
            "f": None
        }
        self.number = number

    # perhaps we want to add an "unbuckling time" for people who are blocking
    # see notebook for why 3 and 5
    def block_time_for_seat(self, seat_letter):
        # we can update the seat occupied here because no one else will get to a seat in this row until after this person sits.
        if seat_letter == "c" or seat_letter == "d":
            return no_block
        elif seat_letter == "b":
            if self.seats_occupied["c"]:
                return side_move_ticks * c_block_b
            else:
                return no_block
        elif seat_letter == "e":
            if self.seats_occupied["d"]:
                return side_move_ticks * c_block_b
            else:
                return no_block
        elif seat_letter == "a":
            # should be similar if just b or both b and c occupied
            if self.seats_occupied["b"]:
                if self.seats_occupied["c"]:
                    return side_move_ticks * bc_block_a
                else:
                    return side_move_ticks * b_block_a
            elif self.seats_occupied["c"]:
                return side_move_ticks * c_block_b
            else:
                return no_block
        elif seat_letter == "f":
            if self.seats_occupied["e"]:
                if self.seats_occupied["d"]:
                    return side_move_ticks * bc_block_a
                else:
                    return side_move_ticks * b_block_a
            elif self.seats_occupied["d"]:
                return side_move_ticks * c_block_b
            else:
                return no_block

class Passenger(object):
    """Represents a passenger and the way they
    move through the plane

    Attributes:
    assigned_seat: an int describing row number
    """
    def __init__(self, assigned_seat, luggage_time):
        self.assigned_seat = assigned_seat
        self.luggage_time = luggage_time
        self.current_row = None
        self.current_seat = None
        self.seated = False
        self.wait_in_aisle_time = 0
        self.reached_row = False

    def update(self):
        if not self.seated:
            if self.assigned_seat[0] == self.current_row.number:
                if not self.reached_row:
                    self.reached_row = True
                    self.wait_in_aisle_time = self.current_row.block_time_for_seat(self.assigned_seat[1])
                if self.luggage_time <= 0:
                    if self.wait_in_aisle_time <= 0:
                        self.seated = True
                        self.current_row.aisle_occupied = None
                        self.current_row.seats_occupied[self.assigned_seat[1]] = True
                    else:
                        if self.wait_in_aisle_time > 2 and self.current_row.next_row is not None and self.current_row.next_row.aisle_occupied is not None:
                            self.wait_in_aisle_time += 1
                        self.wait_in_aisle_time -= 1
                else:
                    self.luggage_time -= 1

            else:
                if self.current_row.next_row.aisle_occupied is not None:
                    pass
                else:
                    self.current_row.aisle_occupied = None
                    self.current_row = self.current_row.next_row
                    self.current_row.aisle_occupied = self


# Runs a single iteration of the simulation,
# updating each passenger in order from the front
# of the queue to the back of the queue.
def iterate(queue):
    for passenger in queue:
        passenger.update()


# Creates a plane with a given number of rows,
# and ties 
def instantiate_plane(num_rows):
    # Create a dummy row for the plane
    rows = [Row(i) for i in range(num_rows + 1)]
    for i in range(len(rows) - 1):
        rows[i].next_row = rows[i + 1]
    return rows

def disp_x(occupant):
    return "o" if occupant is not None else " "

def print_plane(plane, tick):
    print "Plane at tick " + str(tick)
    s = ""
    for r in plane[1:]:
        s = "|" + disp_x(r.seats_occupied["a"]) + "|" + disp_x(r.seats_occupied["b"]) + "|" + disp_x(r.seats_occupied["c"]) + "| " + disp_x(r.aisle_occupied     ) + " |" + disp_x(r.seats_occupied["d"]) + "|" + disp_x(r.seats_occupied["e"]) + "|" + disp_x(r.seats_occupied["f"]) + "|"
        print s
    time.sleep(simulation_time_step)

# Runs a simulation for a given plane and passenger
# configuration
def simulation(queue, plane, verbose):
    for passenger in queue:
        passenger.current_row = plane[0]
    tick = 0
    while any(not passenger.seated for passenger in queue):
        iterate(queue)
        if verbose:
            print_plane(plane, tick)
        tick += 1
    return tick


def main():
    pass

if __name__ == '__main__':
    main()
