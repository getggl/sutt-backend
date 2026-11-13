# BITS Cab Allotter (SUTT Task 1)


## How to run
Requires Python 3 and no external packages. Keep `main.py`, `ctxt.py` and `cabs.json` in the same folder, then run:

```
python main.py
```

On the first run the cabs are loaded from `cabs.json`. After that, the app resumes from `state.json`. Delete `state.json` to start fresh.


### Syntax for cabs.json
```json
[
    {
        "driver_name": "Rob",
        "capacity": 4,
        "destination": "delhi",
        "time_slot": "morning",
        "has_left": false,
        "students": []
    },
    {
        "driver_name": "Bob",
        "capacity": 4,
        "destination": "delhi",
        "time_slot": "afternoon",
        "has_left": false,
        "students": []
    }
]
``` 
It consists of a simple array of dictionaries containing each cab/driver's details

### Syntax for state.json
```json
{
    "requests": [
        {
            "name": "isha",
            "destination": "jaipur",
            "time_slot": "evening",
            "year": 4,
            "timestamp": "2026-11-07T21:41:13.287233"
        },
        {
            "name": "dev",
            "destination": "jaipur",
            "time_slot": "evening",
            "year": 2,
            "timestamp": "2026-11-07T21:41:24.901534"
        }
    ],
    "cabs": []
}
```

The "cabs" array is the same as cabs.json, except it's students property may be non empty and contain the details of the students that have been allotted that cab

The requests array consits dictionaries with the details of each cab request, with the timestamp of when the request/student was registered

JSON was picked for this because it's very convenient to express class instances as dictionaries which can be easily stored in JSON format, and this also makes it easy to go through the data without using the program. It is also human readable unlike picke.


### Navigating through the application:
#### 1) Add new student entry
Allows you to create a new request by providing name and other details
#### 2) View cab allotment
Allows you to preview allotted cabs
#### 3) Dispatch cabs
Allows you to dispatch a cab by providing it's index
#### 4) Quit
Quits the program while saving the progress in state.json
Control+c also has the same effect


## Questions

### 1) What happens if a cab leaves with just 1 or 2 students?
The cab's has_left parameter changes to True and no new students can be added to it even if max capacity hasn't been reached. Those students are removed from the active requests array as well

### 2) What if every cab for a trip (or every cab, full stop) has already left and new requests keep coming?
They aren't alloted a cab but a counter in the 2nd section shows a count of such people, indirectly hence informing them. They may also see in the view cabs section that they haven't been allotted a cab

### 3) If two students are in the same year, how do you make sure the one who asked first gets the seat?
The requests array is sorted firstly based on the year (5>4>3>2>1) and then based on the timestamp incase the year results in a tie. This is done using python's inbuilt `sorted` function and a simple lambda function declaration `sorted(state["requests"], key=lambda r: (-r.year, r.timestamp))`

### 4) Time complexity
i) Adding a request is O(1) in time, adding n requests is O(n) in time, but saving (write_state()) is also O(n) in time which is called from within menu_add_student() so in total effect, adding a student + saving is O(n^2) in time

Proof:
say we start from 0 and add 1000 requests one by one. The first request takes O(1) to add and and O(1) to save, second will take O(1) to take and O(2) to save (O(2) doesn't mean anything, think of it as O(n) with n=2). In turn it becomes 1+2+3...n -> n(n+1)/2 -> O(n^2)

ii) Sending off one cab is O(n) in time, it only requirs flipping the has_left bool to `True` and removing the students from the requests list (O(nlogn) if you count the time taken to resort the requests when the `Dispatch cabs` menu is opened)

iii) Finding an open cab is effectively O(nlogn + n\*c) in terms of time complexity. This is because it first runs timsort through the request list and then iterates through it and in turn iterates through every cab for every iteration in the sorted requests list. This makes it effectively O(nlogn+n\*c) in time complexity (algebric sum). Often times c can be ignored and this can be approximated to O(nlogn)