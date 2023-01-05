import csv
import Truck
import datetime
import CSV_Utilities
from HashMap import HashMap
from Package import Package

# Aidan Morrison
# Student ID: 003658025


# Creating lists of values from Addresses.csv and Distances.csv.
address_table = CSV_Utilities.CSV_Utilities.csv_to_list("CSV_files/Addresses.csv")
distance_table = CSV_Utilities.CSV_Utilities.csv_to_list("CSV_files/Distances.csv")


# This method is used to convert the expected delivery time string from the Packages.csv file to a
# delta time object. This allows you to use logical comparison operators
def convert_expected_delivery_time(delivery_time):
    if delivery_time == "EOD":
        return datetime.timedelta(hours=17)
    elif delivery_time == "9:00 AM":
        return datetime.timedelta(hours=9)
    elif delivery_time == "10:30 AM":
        return datetime.timedelta(hours=10, minutes=30)


# Adds all the package data from Packages.csv to package objects and then adds them to a hashmap.
def get_packages(package_hashmap):
    with open("CSV_files/Packages.csv", encoding='utf-8-sig') as packages_data:
        packages = csv.reader(packages_data, delimiter=";")
        for package in packages:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            # Convert_expected_delivery time is used here to convert the string value into a deltatime object.
            # This is so the package arrival time can be compared to the deadline to make sure the package
            # was delivered on time.
            pExpected_delivery = convert_expected_delivery_time(package[5])
            pWeight = package[6]
            pStatus = "At the hub"

            p = Package(pID, pAddress, pCity, pState, pZipcode, pExpected_delivery, pWeight, pStatus)

            package_hashmap.insert(pID, p)


# Returns distance between two addresses using two address numbers.
def calculate_distance(point_a, point_b):
    return float(distance_table[point_a][point_b])


# Takes a string literal representing an address and compares it to each entry in the  address table returning the
# matching address ID Integer. This process take O(n) time to complete as it has to iterate through every row linearly
# until the matching string address is found.
def address_to_number(address):
    for row in address_table:
        if address not in row[2]:
            continue
        else:
            return int(row[0])


# This sorting method uses the nearest neighbor algorithm. Checking the distance to every connected node then moving to
# the closest node. Removing every node after visiting it. This runs in O(n^2) time because for every point you must
# visit every other connected node to compare distance.
def sort_packages_by_nearest_neighbor(truck):
    while len(truck.truckContents) > 0:
        nearest_distance = 30
        nearest_package = None

        for package in truck.truckContents:
            # Correcting package number 9's address at 10:20 when truck 3 leaves.
            if package.ID == 9:
                package.address = "410 S State St"
            if calculate_distance(address_to_number(truck.location),
                                  address_to_number(package.address)) <= nearest_distance:
                nearest_distance = calculate_distance(address_to_number(truck.location),
                                                      address_to_number(package.address))
                nearest_package = package

        # Setting truck location to address of the closest package. Then deleting the package from the truck_contents
        # and adding it to the truck delivery_log
        truck.location = nearest_package.address
        truck.delivery_queue.enqueue(nearest_package)
        truck.truckContents.remove(nearest_package)

    # Setting truck location back to hub
    truck.location = '4001 South 700 East'


# This method takes a list of integers representing package IDs and uses those IDs as  keys to access the respective
# package object stored as values in the package_hash_map. This runs in O(n) time as hash map access is constant,
# however you must do this for each element of the load list passed as an argument.
def load_packages_into_bin(load, hash_map):
    bin = []
    for id in load:
        bin.append(hash_map.lookup(id))
    return bin


def deliver_packages(truck, package_hashmap):
    distance = 0

    while not truck.delivery_queue.is_empty():
        distance = calculate_distance(address_to_number(truck.location),
                                      address_to_number(truck.delivery_queue.peek().address))
        truck.mileage += distance
        truck.time += datetime.timedelta(hours=distance / truck.averageSpeed)
        truck.location = truck.delivery_queue.peek().address

        # Updating arrival time for the package object in the package hashmap
        package_hashmap.lookup(truck.delivery_queue.peek().ID).arrival_time = truck.time
        # Updating departure time for package based on truck departure time
        package_hashmap.lookup(truck.delivery_queue.peek().ID).departure_time = truck.departure_time

        # Removing package from queue
        truck.delivery_queue.dequeue()

    # Returning truck back to the hub and adding time/ mileage to the truck
    distance = calculate_distance(address_to_number(truck.location), 0)
    truck.mileage += distance
    truck.time += datetime.timedelta(hours=distance / truck.averageSpeed)
    truck.location = '4001 South 700 East'


# The lists are fed into load Packages_into_bin which translates these package ID integers into packages and loads them
# into their respective trucks. The process is O(1) constant time to manually load each trucks associated package IDs.
truck_load1 = [15, 14, 19, 13, 16, 37, 34, 29, 30, 7, 1, 24]
truck_load2 = [3, 25, 28, 4, 33, 38, 40, 31, 32, 8, 2, 36, 11]
truck_load3 = [9, 10, 35, 6, 26, 12, 20, 5, 17, 39, 27, 18, 22, 23, 21]

# Creating a hashmap to load the packages into from the csv file
package_hashmap = HashMap()
# Loading packages into package_hashmap from package.csv
get_packages(package_hashmap)

# Time set to 8:00 because this truck contains most of the packages that need to be delivered by 10:30
truck1 = Truck.Truck(load_packages_into_bin(truck_load1, package_hashmap), datetime.timedelta(hours=8))

# Time set to 9:05 am because it contains the packages that arrive at 9:05 am
truck2 = Truck.Truck(load_packages_into_bin(truck_load2, package_hashmap), datetime.timedelta(hours=9, minutes=5))

# Time set to 10:20 because it contains package number 9 which has the incorrect address that can only be corrected at
# 10:20 am
truck3 = Truck.Truck(load_packages_into_bin(truck_load3, package_hashmap), datetime.timedelta(hours=10, minutes=20))

# Sorting each trucks contents by nearest neighbor
sort_packages_by_nearest_neighbor(truck1)
sort_packages_by_nearest_neighbor(truck2)
sort_packages_by_nearest_neighbor(truck3)

# Delivering each truck of packages
deliver_packages(truck1, package_hashmap)
deliver_packages(truck2, package_hashmap)
# Truck 3 only departs when truck1 or truck2 have returned to the hub
truck3.time = min(truck1.time, truck2.time)
deliver_packages(truck3, package_hashmap)


# Used to move between different user menu options
def clear():
    for x in range(1, 50):
        print("")


def main_menu(truck1, truck2, truck3, package_hash_map):
    print('===================================================================================')
    print('                     WGUPS Parcel Service Route Manager                           ')
    print('===================================================================================')
    print("Options: ")
    print("1: Route Report")
    print("2: Generate Package Report")
    print("3: Search for package by ID")
    print("4: Exit")

    user_input = input("Enter the number for option you would like: ")
    # Entering '1' opens the generate_route_report interface.
    if user_input == "1":
        generate_route_report(truck1, truck2, truck3, package_hash_map)
    # Entering '2' opens the generate_package_report interface.
    elif user_input == "2":
        generate_package_report(truck1, truck2, truck3, package_hash_map)
    # Entering '3' exits the program.
    elif user_input == "3":
        search_package_by_id(truck1, truck2, truck3, package_hash_map)
    else:
        exit()


# method used to open generate route report interface.
def generate_route_report(truck1, truck2, truck3, package_hash_map):
    clear()
    # This Variable is used to represent whether all packages where  delivered by their expected delivery time or not.
    all_packages_on_time = True
    # Lists total mileage of all three trucks combined.
    print(f"Total Mileage: {truck1.mileage + truck2.mileage + truck3.mileage}")
    print("")
    # Lists end of route time and mileage  for each  individual truck.
    print(f"Truck 1 finished it's route at {truck1.time} with a mileage of {truck1.mileage}.")
    print(f"Truck 2 finished it's route at {truck2.time} with a mileage of {truck2.mileage}.")
    print(f"Truck 3 finished it's route at {truck3.time} with a mileage of {truck3.mileage}.")

    # Loops through all the packages in the hash table comparing the arrival time to the expected delivery time
    # ensuring that all packages were delivered on time.
    for x in range(1, 41):
        if package_hash_map.lookup(x).arrival_time <= package_hash_map.lookup(x).expected_delivery:
            continue
        else:
            all_packages_on_time = False
            break

    # Changes the report based on whether all packages made it to their destination on time or not.
    if all_packages_on_time:
        print("")
        print("All packages were delivered on time!")
        print("")
    else:
        print("")
        print("Some packages were delivered late.")
        print("")

    user_input = input("enter 'x' to return to the main menu: ")
    # Entering 'x' returns the user to the main menu interface.
    if user_input == "x":
        clear()
        main_menu(truck1, truck2, truck3, package_hash_map)
    # Does nothing other than generating the same report again.
    else:
        print("Invalid entry try again.")
        generate_route_report(truck1, truck2, truck3, package_hash_map)


# method used to open generate package report interface.
def generate_package_report(truck1, truck2, truck3, package_hash_map):
    clear()
    print("To generate a package report enter a time range you would like to generate a package report for.")
    time1 = input("Enter a the first time you would like to filter by in military format HH:MM: ")

    # Converts string entered by user into a timedelta object, so it can use comparison operators in the update_status
    # method.
    h, m = time1.split(":")
    time1_converted = datetime.timedelta(hours=int(h), minutes=int(m))
    print("_______________________________________________________________________________________________________")

    for x in range(1, 41):
        package_hash_map.lookup(x).update_status(time1_converted)
        print(package_hash_map.lookup(x))

    generate_another_report = input("Would you like to generate another report? Type 'y' for yes and 'n' for no.")

    if generate_another_report == 'y':
        generate_route_report(package_hash_map)
    else:
        clear()
        main_menu(truck1, truck2, truck3, package_hash_map)


def search_package_by_id(truck1, truck2, truck3, package_hash_map):
    clear()
    user_input = int(input("Enter a package ID you would like to search: "))

    print("")
    print(package_hash_map.lookup(user_input))
    print("")
    user_input = input("Would you like to look up another package? enter 'y' or 'n'.")

    if user_input == "y":
        search_package_by_id(truck1, truck2, truck3, package_hash_map)
    else:
        main_menu(truck1, truck2, truck3, package_hash_map)


# Runs the user interface.
main_menu(truck1, truck2, truck3, package_hashmap)
