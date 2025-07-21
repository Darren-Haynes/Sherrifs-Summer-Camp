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
    camp.assign_water()
    camp.print_schedule(bounds=True)
    camp.output_to_csv()
