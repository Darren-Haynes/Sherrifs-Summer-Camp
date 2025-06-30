from collections import OrderedDict
import random
import activities


class SummerCamp:
    def __init__(self) -> None:
        self.main_data = self.instantiate_data()
        self.land = activities.land
        self.land_totals = self.calc_land_totals()
        self.assigned_activity = {k: v[0] for k, v in self.main_data.items()}
        self.land_1st_choice_totals = self.assigned_activity_totals()
        self.land_below_min, self.land_no_votes = self.calc_land_below_min()
        self.land_above_max = self.calc_land_above_max()
        self.land_inbetween = self.filter_land_inbetween()
        self.land_9am = activities.nineAM_land
        self.land_10am = activities.tenAM_land
        self.land_9am_count = 0
        self.land_10am_count = 0

    def instantiate_data(self):
        data = {}
        with open("Data/orig-data.txt", "r") as file:
            lines = file.readlines()
            random.shuffle(lines)
            for line in lines:
                sep = line.strip().split(",")
                data[sep[0]] = sep[1:]
        return data

    def filter_land_inbetween(self):
        inbetween = {}
        for activity in self.land.keys():
            if (
                activity not in self.land_below_min
                and activity not in self.land_above_max
                and activity not in self.land_no_votes
            ):
                shortfall = (
                    self.land[activity][1] - self.land_1st_choice_totals[activity]
                )
                if shortfall < 0:
                    shortfall = (
                        self.land[activity][1] * 2
                        - self.land_1st_choice_totals[activity]
                    )

                inbetween[activity] = shortfall
        return inbetween

    def calc_land_totals(self):
        totals = {}
        for activity in self.land:
            totals[activity] = 0
        for data in self.main_data.values():
            for activity in data[:3]:
                totals[activity] += 1
        return totals

    def assigned_activity_totals(self):
        totals = {}
        for activity in self.land:
            totals[activity] = 0
        for data in self.assigned_activity.values():
            totals[data] += 1
        return totals

    def calc_land_below_min(self):
        below_min = []
        zero_votes = []
        for activity, total in self.land_1st_choice_totals.items():
            minimum = self.land[activity][0]
            if total == 0:
                zero_votes.append([activity, total - minimum])
                continue
            if self.land[activity][2] == 2:
                minimum *= 2
            if total < minimum:
                below_min.append([activity, total - minimum])
        below_min.sort(key=lambda x: x[1])
        zero_votes.sort(key=lambda x: x[1], reverse=True)

        below_dict = OrderedDict({k: v for (k, v) in below_min})
        zero_dict = OrderedDict({k: v for (k, v) in zero_votes})
        return below_dict, zero_dict

    def calc_land_above_max(self):
        above_max = []
        for activity, total in self.land_1st_choice_totals.items():
            maximum = self.land[activity][1]
            if self.land[activity][2] == 2:
                maximum *= 2
            if total > maximum:
                above_max.append([activity, total - maximum])
        above_max.sort(key=lambda x: x[1], reverse=True)
        above_dict = OrderedDict({k: v for (k, v) in above_max})
        return above_dict

    def second_choice_names(self, activity):
        names = []
        for name, choices in self.main_data.items():
            if choices[1] == activity:
                print(name)
                names.append(name)

                # random.choices(names, k=i)

    def get_above_names(self, num):
        above = self.land_above_max.keys()
        below = self.land_below_min.keys()
        names = []
        for name, activitys in self.main_data.items():
            if activitys[0] in above:
                if activitys[num] in below:
                    names.append([name, activitys[num]])
        return names

    def assign_names(self, name, activity):
        if self.land[activity][2] == 0:
            self.land_9am[activity].append(name)

    def update_assigned_activity(self, names):
        for name in names:
            self.assigned_activity[name[0]] = name[1]

    def choice_in_land_below_min(self, name, choice, main_activity):
        self.land_below_min[choice] += 1
        self.assigned_activity[name] = choice
        self.land_1st_choice_totals[choice] += 1
        self.land_1st_choice_totals[main_activity] -= 1
        self.land_above_max[main_activity] -= 1

        if self.land_below_min[choice] == 0:
            del self.land_below_min[choice]
        if self.land_above_max[main_activity] == 0:
            del self.land_above_max[main_activity]
            return True
        return False

    def choice_in_land_below_min_and_below_max(self, name, choice, main_activity):
        # potential bug, not doubling for 9am and 10am combined
        self.assigned_activity[name] = choice
        self.land_1st_choice_totals[choice] += 1
        self.land_1st_choice_totals[main_activity] -= 1
        self.land_above_max[main_activity] -= 1
        if self.land_above_max[main_activity] == 0:
            del self.land_above_max[main_activity]
            return True
        return False

    def find_matching_inbetween(self, choices, main_activity):
        print("I made it")
        print(main_activity)
        for name, choice in choices:
            if choice in self.land_inbetween:
                self.assigned_activity[name] = choice
                self.land_1st_choice_totals[choice] += 1
                self.land_1st_choice_totals[main_activity] -= 1
                self.land_above_max[main_activity] -= 1
                self.land_inbetween[choice] -= 1
                if self.land_inbetween[choice] == 0:
                    del self.land_inbetween[choice]
                if self.land_above_max[main_activity] == 0:
                    del self.land_above_max[main_activity]
                    return True
        return False

    def find_matching_below_min(self, choices, main_activity):
        for name, choice in choices:
            if choice in self.land_below_min:
                if self.choice_in_land_below_min(name, choice, main_activity):
                    return True

            elif self.land_1st_choice_totals[choice] < self.land[choice][1]:
                if self.choice_in_land_below_min_and_below_max(
                    name, choice, main_activity
                ):
                    return True
        return False

    def get_2nd_3rd_and_no_choices(self, main_activity, activities):
        activity_list = activities.keys()
        choice2 = []
        choice3 = []
        no_choice = []
        for name, choice1 in self.assigned_activity.items():
            if choice1 == main_activity:
                if self.main_data[name][1] in activity_list:
                    choice2.append([name, self.main_data[name][1]])
                elif self.main_data[name][2] in activity_list:
                    choice3.append([name, self.main_data[name][2]])
                else:
                    no_choice.append(name)
        return choice2, choice3, no_choice

    def above_max_to_not_maxed_out(self, main_activity):
        choice2, choice3, no_choice = self.get_2nd_3rd_and_no_choices(
            main_activity, self.land_inbetween
        )
        if self.find_matching_inbetween(choice2, main_activity):
            return True

        if self.find_matching_inbetween(choice3, main_activity):
            return True

        for name in no_choice:
            # TODO complete this case scenario
            print("NO CHOICE")
            print(name)
        return False

    def above_to_below(self, main_activity):
        choice2, choice3, no_choice = self.get_2nd_3rd_and_no_choices(
            main_activity, self.land_below_min
        )

        if self.find_matching_below_min(choice2, main_activity):
            return True

        if self.find_matching_below_min(choice3, main_activity):
            return True

        for name in no_choice:
            # TODO complete this case scenario
            print("NO CHOICE")
            print(name)
        return False

    def calc_above_and_below(self):
        below_min = abs(sum(self.land_below_min.values()))
        below_max = below_min
        above = sum(self.land_above_max.values())
        for activity in self.land_below_min:
            below_max += self.land[activity][1] - self.land[activity][0]
        return below_min, below_max, above

    def compare_above_to_below(self, main_activity):
        below_min, below_max, above = self.calc_above_and_below()

        # um the sweet spot...
        if below_min <= above <= below_max:
            self.above_to_below(main_activity)
        # remove an activity and recalulate
        elif below_min > above:
            print("below_min > above")
        # find activities not maxed out to move over max activities to.
        elif above > below_max:
            self.above_max_to_not_maxed_out(main_activity)
        else:
            # This shoudn't happen
            pass

    def assign_land(self):
        if self.land_above_max:
            for activity in list(self.land_above_max.keys()):
                self.compare_above_to_below(activity)

        self.assign_land_timeslots()

    def assign_land_timeslots(self):
        both = {}
        not_both = {}
        for name, activity in self.assigned_activity.items():
            if activity in self.land_9am and activity in self.land_10am:
                if self.land_1st_choice_totals[activity] >= self.land[activity][0] * 2:
                    if activity in both:
                        if both[activity]:
                            both[activity] = False
                        else:
                            both[activity] = True
                    else:
                        both[activity] = True
                    if both[activity]:
                        self.land_9am[activity].append(name)
                        self.land_9am_count += 1
                    else:
                        self.land_10am[activity].append(name)
                        self.land_10am_count += 1

                else:
                    if activity in not_both:
                        not_both[activity].append(name)
                    else:
                        not_both[activity] = [name]

            elif activity in self.land_9am:
                self.land_9am[activity].append(name)
                self.land_9am_count += 1
            elif activity in self.land_10am:
                self.land_10am[activity].append(name)
                self.land_10am_count += 1

        if not_both:
            for activity, names in not_both:
                if self.land_9am_count >= self.land_10am_count:
                    self.land_10am[activity] = names
                    self.land_10am_count += len(names)
                else:
                    self.land_9am[activity] = names
                    self.land_9am_count += len(names)

    def print_land(self):
        print("*** 9AM LAND ACTIVITIES ***")
        for activity, names in self.land_9am.items():
            if names:
                print(f"{activity.upper()}: {', '.join(names)}")
        print("\n")
        print("*** 10AM LAND ACTIVITIES ***")
        for activity, names in self.land_10am.items():
            if names:
                print(f"{activity.upper()}: {', '.join(names)}")
