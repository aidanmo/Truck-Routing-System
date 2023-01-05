class Package:
    # Constructor used to create a package object.
    def __init__(self, ID, address, city, state, zipcode, expected_delivery, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.expected_delivery = expected_delivery
        self.weight = weight
        self.status = None
        self.departure_time = None
        self.arrival_time = None

    # toString method used to print a Package object as a string listing its attribute values.
    def __str__(self):
        return f"{self.ID} , {self.address}, {self.city}, {self.state}, {self.zipcode}, {self.expected_delivery}, " \
               f"{self.weight}, {self.status}, {self.arrival_time}"

    # Method used to update the status attribute of a Package object by comparing its arrival_time value and departure
    # time value to the deltatime object passed as an argument.
    def update_status(self, time):
        if self.arrival_time <= time:
            self.status = "Arrived"
        elif self.departure_time < time < self.arrival_time:
            self.status = "En Route"
        elif self.departure_time > time:
            self.status = "At the hub"
