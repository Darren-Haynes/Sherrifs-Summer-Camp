land = {
    # tuple[0] min of num of people per land activity
    # tuple[1] max of num of people per land activity
    # tuple[2] 0 = 9am only, 1 = 10am only, 2 = 9am & 10am activities
    "basketball": [6, 12, 0],
    "volleyball": [6, 12, 0],
    "soccer": [6, 12, 0],
    "archery": [8, 16, 2],
    "arts": [4, 10, 2],
    "hiking": [4, 6, 2],
    "cheer": [6, 12, 0],
    "pickleball": [4, 12, 1],
    "lacrosse": [6, 12, 1],
    "football": [6, 12, 1],
    "yoga": [6, 10, 1],
    "frisbee": [3, 8, 1],
}

water = {
    # tuple[0] min of num of people per water activity
    # tuple[1] max of num of people per water activity
    "swimming": (6, 16, 2),
    "fishing": (4, 7, 2),
    "canoe": (6, 10, 2),
    "snorkle": (4, 8, 2),
    "sailing": (6, 16, 2),
    "paddleboard": (4, 8, 2),
    "kayak": (6, 8, 2),
}

nineAM_land = {
    # Land activities offered for the 9am slot
    # Boolean represents if the time slot is full (True)
    "basketball": [],
    "volleyball": [],
    "soccer": [],
    "archery": [],
    "arts": [],
    "hiking": [],
    "cheer": [],
}

nineAM_water = {
    # Water activities offered for the 9am slot
    "swimming": [],
    "fishing": [],
    "canoe": [],
    "kayak": [],
    "snorkle": [],
    "sailing": [],
    "paddleboard": [],
}
tenAM_land = {
    # Land activities offered for the 10am slot
    "pickleball": [],
    "lacrosse": [],
    "football": [],
    "archery": [],
    "arts": [],
    "hiking": [],
    "yoga": [],
    "frisbee": [],
}

tenAM_water = {
    # Water activities offered for the 10am slot
    "swimming": [],
    "fishing": [],
    "canoe": [],
    "kayak": [],
    "snorkle": [],
    "sailing": [],
    "paddleboard": [],
}
