land = {
    # tuple[0] min of num of people per land activity
    # tuple[1] max of num of people per land activity
    # tuple[2] 0 = 9am only, 1 = 10am only, 2 = 9am & 10am activities
    "bball": [6, 12, 0],  # baseball
    "vball": [6, 12, 0],  # volleyball
    "soc": [6, 12, 0],  # soccer
    "arch": [8, 16, 2],  # archery
    "art": [4, 10, 2],  # art
    "hike": [4, 6, 2],  # hiking
    "cheer": [6, 12, 0],  # cheer
    "pball": [4, 12, 1],  # pickleball
    "lax": [6, 12, 1],  # lacrosse
    "fball": [6, 12, 1],  # football
    "yoga": [6, 10, 1],  # yoga
    "fris": [3, 8, 1],  # frisbee
}

water = {
    # tuple[0] min of num of people per water activity
    # tuple[1] max of num of people per water activity
    # tuple[2] 0 = 9am only, 1 = 10am only, 2 = 9am & 10am activities
    "swim": (6, 16, 2),  # swimming
    "fish": (4, 7, 2),  # fishing
    "canoe": (6, 10, 2),  # canoe
    "snork": (4, 8, 2),  # snorkle
    "sail": (6, 16, 2),  # sailing
    "pboard": (4, 8, 2),  # paddleboard
    "kayak": (6, 8, 2),  # kayak
}

nineAM_land = {
    # Land activities offered for the 9am slot
    # Boolean represents if the time slot is full (True)
    "bball": [],
    "vball": [],
    "soc": [],
    "arch": [],
    "art": [],
    "hike": [],
    "cheer": [],
}

nineAM_water = {
    # Water activities offered for the 9am slot
    "swim": [],
    "fish": [],
    "canoe": [],
    "kayak": [],
    "snork": [],
    "sail": [],
    "pboard": [],
}
tenAM_land = {
    # Land activities offered for the 10am slot
    "pball": [],
    "lax": [],
    "fball": [],
    "arch": [],
    "art": [],
    "hike": [],
    "yoga": [],
    "fris": [],
}

tenAM_water = {
    # Water activities offered for the 10am slot
    "swim": [],
    "fish": [],
    "canoe": [],
    "kayak": [],
    "snork": [],
    "sail": [],
    "pboard": [],
}
