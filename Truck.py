import Queue

class Truck:
    # Constructor used to create a truck object.
    def __init__(self, truckContents, departure_time):
        self.maxPackages = 16
        self.averageSpeed = 18.0
        self.truckContents = truckContents
        self.delivery_queue = Queue.Queue()
        self.location = '4001 South 700 East'
        self.mileage = 0.0
        self.departure_time = departure_time
        self.time = departure_time

    # toString method used to print a Truck object as a string listing its attribute values.
    def __str__(self):
        return f'{self.maxPackages}, {self.averageSpeed}, {self.truckContents}, {self.delivery_queue} ' \
               f'{self.location}, {self.mileage}, {self.time}'
