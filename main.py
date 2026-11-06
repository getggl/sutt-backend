import json
import os
import datetime



state = {}
file_name = "state.json"



class RideRequest:
    def __init__(self, name: str, destination: str, time_slot: str, year: int):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.timestamp = datetime.datetime.now()

    def __str__(self):
        return f"Name:{self.name}, Year:{self.year}), Dest:{self.destination} Slot:{self.time_slot}"


class Cab:
    def __init__(self, driver_name: str, capacity: int, destination: str, time_slot: str):
        self.driver_name = driver_name
        self.capacity = capacity  # 1 to 4
        self.destination = destination
        self.time_slot = time_slot
        self.has_left = False  # tracks whether the cab has departed yet
        self.students = []     # list of students currently in the cab

    def is_full(self) -> bool:
        return len(self.students) >= self.capacity

    def __str__(self):
        status = "Left" if self.has_left else "Open"
        return (f"Driver: {self.driver_name} | Dest: {self.destination} | "
                f"Slot: {self.time_slot}, Seats: {len(self.students)}/{self.capacity}, Status: {status}")



def write_state(s=state):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=4)


def read_state():
    with open(file_name, "r", encoding="utf-8") as file:
        phase = json.load(file)



while True: # main loop
    print("Select option:")
    print("1) Add new student entry")
    print("2) View cab allotment")
    print("3) Dispatch cabs")
    print("4) Quit")
    
    i = input("Selected option: ")
    
    if i == "1":
        print(i) # move to new student section
        os.system('cls' if os.name == 'nt' else 'clear')
    elif i == "2":
        print(i)
    elif i == "3":
        print(i)
    elif i == "4":
        exit()
    else:
        print("Invalid choice, try again")
