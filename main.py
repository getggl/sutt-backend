import json
import os
import sys
import datetime
import signal
import atexit

import ctxt



state = {
    "requests": [],
    "cabs" : []
}
file_name = "state.json"
cab_file_name = "cabs.json"



class RideRequest:
    def __init__(self, name: str, destination: str, time_slot: str, year: int, timestamp=None):
        if timestamp and isinstance(timestamp, str):
            timestamp = datetime.datetime.fromisoformat(timestamp)
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.timestamp = timestamp if timestamp is not None else datetime.datetime.now()

    def __str__(self):
        return f"Student: {self.name} | Year: {self.year} | Dest: {self.destination} | Slot: {self.time_slot}"
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "destination": self.destination,
            "time_slot": self.time_slot,
            "year": self.year,
            "timestamp": self.timestamp.isoformat()
        }


class Cab:
    def __init__(self, driver_name: str, capacity: int, destination: str, time_slot: str, has_left=False, students=None):
        self.driver_name = driver_name
        self.capacity = capacity
        self.destination = destination
        self.time_slot = time_slot
        self.has_left = has_left
        self.students = students if students is not None else []

    def is_full(self) -> bool:
        return len(self.students) >= self.capacity

    def __str__(self):
        status = "Left" if self.has_left else "Open"
        return f"Driver: {self.driver_name} | Dest: {self.destination} | Slot: {self.time_slot} | Seats: {len(self.students)}/{self.capacity} | [{status}]"

    def to_dict(self) -> dict:
        return {
            "driver_name": self.driver_name,
            "capacity": self.capacity,
            "destination" : self.destination,
            "time_slot" : self.time_slot,
            "has_left" : self.has_left,
            "students" : [student.to_dict() for student in self.students]
        }


def write_state():
    json_state = {
        "requests": [req.to_dict() for req in state["requests"]],
        "cabs": [cab.to_dict() for cab in state["cabs"]]
    }
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(json_state, file, indent=4)
    

def read_state():
    with open(file_name, "r", encoding="utf-8") as file:
        json_state = json.load(file)
        state["requests"] = [RideRequest(**req) for req in json_state["requests"]]
        state["cabs"] = [Cab(**cab) for cab in json_state["cabs"]]
        for cab in state["cabs"]:
            cab.students = [RideRequest(**student) for student in cab.students]


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input(ctxt.cyan("\nPress Enter to return to main menu..."))


def clean_exit(signum, frame):
    print(ctxt.cyan("\nSIGINT: Saving state..."))
    write_state()
    print(ctxt.green("State successfully saved. Exiting..."))
    sys.exit(0)


def allot_cabs():
    for cab in state["cabs"]:
        if not cab.has_left:
            cab.students = []
    sorted_requests = sorted(state["requests"], key=lambda r: (-r.year, r.timestamp))
    for request in sorted_requests:
        for cab in state["cabs"]:
            if (cab.destination == request.destination and
                cab.time_slot == request.time_slot and
                not cab.is_full() and
                not cab.has_left):
                cab.students.append(request)
                break


def init():
    if os.path.exists(file_name):
        try:
            read_state()
            print(ctxt.green("✔ Successfully loaded application state from state.json"))
        except Exception as e:
            print(ctxt.red(f"✖ Error loading state.json: {e}"))
            sys.exit(1)
    elif os.path.exists(cab_file_name):
        try:
            with open(cab_file_name, "r", encoding="utf-8") as file:
                cab_list_data = json.load(file)
            state["cabs"] = [Cab(**cab) for cab in cab_list_data]
            state["requests"] = []
            print(ctxt.green("✔ Successfully loaded initial cabs from cabs.json"))
        except Exception as e:
            print(ctxt.red(f"✖ Error loading cabs.json: {e}"))
            sys.exit(1)
    else:
        print(ctxt.red("✖ Neither 'state.json' nor 'cabs.json' found, exiting..."))
        sys.exit(1)
    atexit.register(write_state)
    signal.signal(signal.SIGINT, clean_exit)


def main():
    clear()
    print(ctxt.cyan("========================================"))
    print(ctxt.cyan("|      BITS CAB POOL MATCHER           |"))
    print(ctxt.cyan("========================================"))
    print(" 1) Add new student entry")
    print(" 2) View cab allotment preview")
    print(" 3) Dispatch cabs")
    print(" 4) Quit application")
    print(ctxt.cyan("----------------------------------------"))
    
    i = input(ctxt.yellow("Select option (1-4): ")).strip()
    
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
        print(ctxt.cyan("Saving and quitting application..."))
        write_state()
        sys.exit()
    else:
        clear()
        print(ctxt.red("✖ Invalid choice. Please enter a number between 1 and 4."))
        pause()


def menu_add_student():
    print(ctxt.cyan("- ADD NEW RIDE REQUEST"))
    name = input("Enter student name: ").strip()
    destination = ""
    time_slot = ""
    year = -1

    while True:
        destination = input("Enter destination (Delhi / Jaipur): ").strip().lower()
        if destination in ["delhi", "jaipur"]:
            break
        else:
            print(ctxt.red("✖ Invalid destination. Please enter either Delhi or Jaipur."))

    while True:
        time_slot = input("Enter time slot (Morning / Afternoon / Evening / Night): ").strip().lower()
        if time_slot in ["morning", "afternoon", "evening", "night"]:
            break
        else:
            print(ctxt.red("✖ Invalid time slot."))
    
    while True:
        year = input("Enter academic year (1 to 5): ").strip()
        if year in ["1", "2", "3", "4", "5"]:
            year = int(year)
            break
        else:
            print(ctxt.red("✖ Invalid year. Year must be between 1 and 5."))
    
    state["requests"].append(RideRequest(name, destination, time_slot, year))
    clear()
    print(ctxt.green(f"✔ Request successfully registered!"))
    print(ctxt.magenta(f"Timestamp: {state["requests"][-1].timestamp.strftime('%Y-%m-%d %H:%M:%S')}"))
    pause()


def menu_view_cabs():
    allot_cabs()
    print(ctxt.cyan("- CAB ALLOTMENT PREVIEW"))
    for cab in state["cabs"]:
        if cab.has_left:
            print(ctxt.red(f"{cab} [🔒]"))
        else:
            print(ctxt.blue(f"{cab}"))

        if cab.students:
            for student in cab.students:
                print(ctxt.yellow(f"    ↳ {student}"))
        else:
            print(ctxt.magenta("    ↳ No students assigned yet"))
    
    print(ctxt.cyan("----------------------------------------"))
    assigned = sum(len(cab.students) for cab in state["cabs"] if not cab.has_left)
    print(ctxt.magenta(f"Total students waiting in queue: {len(state['requests']) - assigned}"))
    pause()


def menu_dispatch():
    allot_cabs()
    print(ctxt.cyan("- DISPATCH CAB MENU"))
    open_cabs = [cab for cab in state["cabs"] if not cab.has_left]
    if len(open_cabs) == 0:
        print(ctxt.red("✖ No open cabs available to dispatch!"))
        pause()
        return
    
    destination = ""
    while True:
        destination = input("Enter destination (Delhi / Jaipur): ").strip().lower()
        if destination in ["delhi", "jaipur"]:
            break
        else:
            print(ctxt.red("✖ Invalid destination. Please enter either Delhi or Jaipur."))

    time_slot = ""
    while True:
        time_slot = input("Enter time slot (Morning / Afternoon / Evening / Night): ").strip().lower()
        if time_slot in ["morning", "afternoon", "evening", "night"]:
            break
        else:
            print(ctxt.red("✖ Invalid time slot."))

    target_cab = None
    for cab in state["cabs"]:
        if cab.destination == destination and cab.time_slot == time_slot and not cab.has_left:
            target_cab = cab
            break

    if not target_cab:
        print(ctxt.red(f"✖ No open cabs found for {destination} ({time_slot})."))
        pause()
        return

    print(ctxt.blue(f"\nFound Open Cab: {target_cab}"))
    if target_cab.students:
        for student in target_cab.students:
            print(ctxt.yellow(f"    ↳ {student}"))
    else:
        print(ctxt.magenta("    ↳ No students assigned yet"))
    
    confirm = input(ctxt.yellow("\nDispatch this cab? (y/n): ")).strip().lower()
    if confirm == 'y':
        target_cab.has_left = True
        for student in target_cab.students:
            if student in state["requests"]:
                state["requests"].remove(student)
        print(ctxt.green(f"✔ Cab driven by {target_cab.driver_name} dispatched successfully!"))
    else:
        print("Dispatch cancelled. Returning to main menu...")
    
    pause()


clear()
init()
while True:
    main()