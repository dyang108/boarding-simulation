class Row(object):
    """Represents one row of the airplane"""
    def __init__(self, number):
        self.next_row = None
        self.occupied = False
        self.number = number


class Passenger(object):
    """Represents a passenger and the way they
    move through the plane

    Arguments:
    assigned_seat: an (x, y) tuple describing row and seat number"""
    def __init__(self, assigned_seat, luggage_time):
        self.assigned_seat = assigned_seat
        self.luggage_time = luggage_time
        self.current_row = None
        self.current_seat = None
        self.seated = False

    def update(self):
        if not self.seated:
            if self.assigned_seat == self.current_row.number:
                if self.luggage_time == 0:
                    self.seated = True
                    self.current_row.occupied = False
                else:
                    self.luggage_time -= 1

            else:
                if self.current_row.next_row.occupied:
                    pass
                else:
                    self.current_row.occupied = False
                    self.current_row = self.current_row.next_row
                    self.current_row.occupied = True


def iterate(queue):
    for passenger in queue:
        passenger.update()


def instantiate_plane(num_rows):
    # Create a dummy row for the plane
    rows = [Row(i) for i in range(num_rows + 1)]
    for i in range(len(rows) - 1):
        rows[i].next_row = rows[i + 1]
    return rows


# Runs a simulation for a given plane and passenger
# configuration
def simulation(queue, plane):
    for passenger in queue:
        passenger.current_row = plane[0]
    time_step = 0
    while any(not passenger.seated for passenger in queue):
        iterate(queue)
        time_step += 1
    return time_step


def main():
    pass


# def main():
#     row = Row()
#     print(row.occupied)

if __name__ == '__main__':
    main()
