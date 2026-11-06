import json
import os
import sys
import datetime
import signal

import ctxt



#signal.signal(signal.SIGINT, sys.exit)


state = {
    "requests": [],
    "cabs" : []
}



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


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')



def init():
    pass


def main():
    print("Select option:")
    print("1) Add new student entry")
    print("2) View cab allotment")
    print("3) Dispatch cabs")
    print("4) Quit")
    
    i = input("Selected option: ")
    
    if i == "1":
        clear()
        menu_add_student()
    elif i == "2":
        clear()
        menu_view_cabs()
    elif i == "3":
        clear()
        menu_dispatch()
    elif i == "4":
        clear()
        print("Quitting...")
        sys.exit()
    else:
        clear()
        print(ctxt.red("Invalid choice, try again"))


def menu_add_student():
    name = input("Enter name of student: ")
    destination = ""
    time_slot = ""
    year = -1

    while True:
        destination = input("Enter destination (Delhi or Jaipur): ").lower()
        if destination in ["delhi", "jaipur"]:
            break
        else:
            print(ctxt.red("Invalid destination. Enter either Delhi or Jaipur"))

    while True:
        time_slot = input("Enter time slot (Morning, Afternoon, Evening, Night): ").lower()
        if time_slot in ["morning", "afternoon", "evening", "night"]:
            break
        else:
            print(ctxt.red("Invalid time slot"))
    
    while True:
        year = input("Enter year (1 to 5): ")
        if year in ["1", "2", "3", "4", "5"]:
            year = int(year)
            break
        else:
            print(ctxt.red("Invalid year. Year must be 1-5"))
    
    state["requests"].append(RideRequest(name, destination, time_slot, year))
    clear()
    print(f"Successfully added! Time stamp: {state["requests"][-1].timestamp}")


def menu_view_cabs():
    pass


def menu_dispatch():
    pass



clear()
init()
while True: # main loop
    main()