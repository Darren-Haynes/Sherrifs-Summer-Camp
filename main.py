from summer_camp import SummerCamp


def activity_count(camp, activity, num=1):
    count = 0
    for name, choice in camp.main_data.items():
        if choice[num] == activity:
            count += 1
    return count


if __name__ == "__main__":
    camp = SummerCamp()
    print(camp.land_inbetween)
    print(camp.land_below_min)
    print(camp.calc_kids_min())
    print(camp.calc_kids_max())
    camp.assign_land()
    camp.print_land(bounds=True)
    print(camp.land_9am_count)
    print(camp.land_10am_count)
    print(camp.land_inbetween)
    # print("WHAT ON EARTH")
    # print(camp.filter_sort_land_inbetween())
