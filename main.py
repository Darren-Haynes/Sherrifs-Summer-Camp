from summer_camp import SummerCamp


def activity_count(camp, activity, num=1):
    count = 0
    for name, choice in camp.main_data.items():
        if choice[num] == activity:
            count += 1
    return count


if __name__ == "__main__":
    camp = SummerCamp()
    camp.assign_land()
    camp.print_land(bounds=True)
    camp.assign_water()
    print(camp.assigned_water_9am_activity)
    print(camp.assigned_water_10am_activity)
    print(len(camp.assigned_water_9am_activity))
    print(len(camp.assigned_water_10am_activity))
