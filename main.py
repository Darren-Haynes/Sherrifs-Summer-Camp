from summer_camp import SummerCamp


if __name__ == "__main__":
    camp = SummerCamp()
    camp.assign_land()
    camp.assign_water()
    camp.print_schedule(bounds=False)
    camp.output_to_csv()
