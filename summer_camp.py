import activities


class SummerCamp:
    def __init__(self) -> None:
        self.main_data = self.instantiate_data()
        self.land = activities.land
        self.land_totals = self.calc_land_totals()
        self.land_1st_choice = self.calc_land_totals(1)
        self.land_below_min, self.land_no_votes = self.calc_land_below_min()
        self.land_above_max = self.calc_land_above_max()

    def instantiate_data(self):
        data = {}
        with open("Data/orig-data.txt", "r") as file:
            for line in file.readlines():
                sep = line.strip().split(",")
                data[sep[0]] = sep[1:]
        return data

    def calc_land_totals(self, upper=3):
        totals = {}
        for activity in self.land:
            totals[activity] = 0
        for data in self.main_data.values():
            for activity in data[:upper]:
                totals[activity] += 1
        return totals

    def calc_land_below_min(self):
        below_min = []
        zero_votes = []
        for activity, total in self.land_1st_choice.items():
            minimum = self.land[activity][0]
            if total == 0:
                zero_votes.append(activity)
                continue
            if self.land[activity][2] == 2:
                minimum *= 2
            if total < minimum:
                below_min.append([activity, total - minimum])
        below_min.sort(key=lambda x: x[1], reverse=True)
        return below_min, zero_votes

    def calc_land_above_max(self):
        above_max = []
        for activity, total in self.land_1st_choice.items():
            maximum = self.land[activity][1]
            if self.land[activity][2] == 2:
                maximum *= 2
            if total > maximum:
                above_max.append([activity, total - maximum])
        above_max.sort(key=lambda x: x[1], reverse=True)
        return above_max
